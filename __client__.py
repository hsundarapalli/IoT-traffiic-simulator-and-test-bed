from Logger import Logger
import socket
from analysis import client_analysis as analysis
from threading import Thread
class client(Logger):
    soc   = None
    ip    =  None
    port  =  None
    __id  =  None
    logger = None
    analysis_list =None
    analysis=None

    def __init__(self, __id):

        self.soc=socket.socket()
        self.__id = __id


    # connect on specified server ip and port
    def connect(self, ip, port):

        self.ip = ip
        self.port = port
        self.soc.connect((ip, port))

        return self.soc

    # overrides the abstract method log in Logger class
    def log(self, msg):

        self.out = f"Client_{self.__id} | " + msg
        self.logger.info(self.out)


    def send(self, msg):

        self.soc.send(bytes(str(msg), "utf-8"))


    def rcv(self):

        msg = self.soc.recv(1024).decode()
        return msg

    def start_simulation(self, analysis_list, simulation_time):

            self.analysis=analysis(analysis_list,simulation_time)

            Thread(target=self.analysis.start_analysis).start()
