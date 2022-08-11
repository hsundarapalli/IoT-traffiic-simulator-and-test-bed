import sys
import logging
import socket
import threading


def usage():
    print("Error: Insufficient arguments")
    print(f"Usage: python3 {sys.argv[0]} </path/to/config/file> <ID>")
    sys.exit(101)


def arg_parse():
    if (len(sys.argv) != 3):
        usage()
    else:
        config_file = sys.argv[1]
        my_id = sys.argv[2]

    return config_file, my_id


def get_pool_type(configs):
    if configs["multiprocessed"] == "True":
        pool_type = 1
    elif configs["multithreaded"] == "True":
        pool_type = 0

    return pool_type

    