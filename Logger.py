import logging

class Logger:
    logger = None
    def log_setup(self, logfile):
        logging.basicConfig(filename=logfile,
                            format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S |',
                            filemode='w')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        return self.logger

    #@abstractmethod
    def log(self, msg):
        pass