"""
Server:
Recieves a number from the client.
Adds 1 to it and send back to the client.

command line arguments :$ code_file config_file
"""
import sys
import time
from threading import Thread
from multiprocessing import Manager, Process
import utils
import configurations
from __server__ import server

my_id = None
config_file = None
logger = None
pool_type = None


# defining the function of the worker
def process_requests(request_queue, processed_queue, worker_id, server):
    while True:

        if request_queue.qsize() == 0:  # checking the queue
            time.sleep(0.1)
        else:
            request_details = request_queue.get()
            client_id = request_details[0]
            received = request_details[1]
            response = received + 1

            # putting in queue after processing
            processed_queue.put(list([client_id, received,
                                      response, worker_id]))


# definition of thread to push the requests
def push_requests(request_queue, client_soc, client_id, server):
    while True:
        request = int(client_soc.recv(1024).decode())
        request_queue.put([client_id, request])
        server.analysis.no_of_requests += 1


def push_requests_to_queue(request_queue, server):
    # iterate over all the client connections
    while True:
        client = server.connections.get()
        client_id = client[0]
        client_soc = client[1]

        # start pushing the requests to the queue
        Thread(target=push_requests,
               args=(request_queue, client_soc, client_id, server,)).start()


# creating the worker based on pool type
def create_worker(worker_id):
    if pool_type == 1:
        Process(target=process_requests,
                args=(request_queue, processed_queue, worker_id, server,)).start()
    else:
        Thread(target=process_requests,
               args=(request_queue, processed_queue, worker_id, server,)).start()


if __name__ == '__main__':

    # allocate shared memory
    request_queue = Manager().Queue()
    processed_queue = Manager().Queue()

    # parse config file
    config_file, my_id = utils.arg_parse()
    configs = configurations.parse(config_file, "server_config")
    ip = configs["ip"]
    port = configs["port"]
    no_of_workers = configs["no_of_workers"]
    logfile = configs["logfile_base"] + str(my_id) + ".log"
    pool_type = utils.get_pool_type(configs)
    simulation_time = configs["simulation_time"]
    analysis_list = configurations.parse(config_file, "server_analysis_list")

    # create and setup the server
    server = server(my_id)
    server.configure(ip, port, simulation_time, analysis_list)

    server.log_setup(logfile)
    server.log("Spawned.")

    server.accept_connections()
    Thread(target=push_requests_to_queue,
           args=(request_queue, server,)).start()

    # creating workers to process the requests (parellalism)
    for worker_id in range(no_of_workers):
        create_worker(worker_id + 1)

    server.send_response(pool_type, processed_queue)


