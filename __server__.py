import time
import socket
from threading import Thread
from Logger import Logger
from queue import Queue
from analysis import server_analysis as analysis
#extending the Logger and Thread classes
class server(Logger,Thread)  :

    # attributes of server
    server_soc  = None
    ip          = None
    port        = None
    __id        = None
    logger      = None
    connections = Queue(maxsize = 1000)
    client_dict = {}
    simulation_time=None
    analysis       = None
    analysis_list  = None
    def __init__(self, __id):

        Thread.__init__(self)
        self.server_soc = socket.socket()
        self.__id       = __id


    def configure(self, ip, port,simulation_time,analysis_list):

        self.ip     = ip
        self.port   = port
        self.simulation_time=simulation_time
        self.analysis_list= analysis_list
        self.analysis = analysis(self.analysis_list,self.simulation_time)
        self.server_soc.bind((ip,port))
        self.server_soc.listen(10)


    # write to logfile
    def log(self, msg):

        self.out = f"Server_{self.__id} | " + msg
        self.logger.info(self.out)

    # start invokes run method to accpet incomming connection requests
    def run(self):
        simulation_started = False

        while True:

            client_soc,client_ip   = self.server_soc.accept()
            client_id              = int(client_soc.recv(1024).decode())
            self.client_dict[client_id] = client_soc
            if(simulation_started == False):
                simulation_started = True
                self.start_simulation()
            self.connections.put([client_id,client_soc])
            self.analysis.no_of_clients +=1

    def accept_connections(self):
        self.start()


    # function to send all the processed requests to the respective clients
    def __send_response(self, pool_type,processed_queue):

        while True:

            if processed_queue.qsize() == 0:
                time.sleep(0.1)
            else :
                request_details  = processed_queue.get()
                client_id        = request_details[0]
                received         = request_details[1]
                response         = request_details[2]
                worker_id        = request_details[3]
                client_soc       = self.client_dict[client_id]
                worker_type      = None

                client_soc.send(bytes(str(response),"utf-8"))
                self.analysis.processed_requests +=1

                if pool_type == 1:
                    worker_type ="Process"
                else :
                    woker_type = "Thread"

                self.log(f"{worker_type}_{worker_id}"+
                    f" Request processed for client{client_id}."+
                    f" Received --{received} | Send -- {response}  ")


    def send_response(self, pool_type,processed_queue):

        Thread(target=self.__send_response,
            args=(pool_type,processed_queue,)).start()

    def start_simulation(self):

            Thread(target=self.analysis.start_analysis).start()
