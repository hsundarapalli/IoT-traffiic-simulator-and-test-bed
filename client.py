"""
Client: sends a number to the server and expects another number in return
"""
import sys
import socket
import logging
import random
import time
import configurations
import utils
from __client__ import client

my_id = None
config_file = None


def run_client(client, my_num):
    start_time = time.time()
    client.send(my_num)
    received = client.rcv()
    end_time = time.time()
    client.log(f"sent {my_num}, received " + received)
    client.analysis.processing_time.append(end_time - start_time)


def traffic_generator(traffic, periodicity):
    while True:

        my_num = random.randint(1, 1000)

        if traffic == "periodic":
            delay = periodicity
        elif traffic == "sporadic":
            delay = random.uniform(0, .05)
        else:
            print("Unsupported Traffic Pattern")
            sys.exit()

        yield (my_num, delay)


if __name__ == "__main__":

    # check arguments and parse config file
    config_file, my_id = utils.arg_parse()
    configs = configurations.parse(config_file, "client_config")
    s_ip = configs["server_ip"]
    s_port = configs["server_port"]
    logfile = configs["logfile_base"] + str(my_id) + ".log"
    traffic = configs["traffic"]
    periodicity = configs["periodicity"]
    simulation_time = configs["simulation_time"]
    analysis_list = configurations.parse(config_file, "client_analysis_list")

    # create client and connect to client
    client = client(my_id)
    client.connect(s_ip, s_port)

    client.log_setup(logfile)
    client.log("Spawned.")
    client.start_simulation(analysis_list, simulation_time)
    client.send(my_id)

    # traffic generator
    for Traffic in traffic_generator(traffic, periodicity):
        num = Traffic[0]
        delay = Traffic[1]
        time.sleep(delay)
        run_client(client, num)

