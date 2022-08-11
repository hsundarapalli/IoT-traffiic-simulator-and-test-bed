import time
import sys


# client statistics
class client_analysis():
    analysis_dict = {

        "average_time": None,
        "maximum_time": None,
        "minimum_time": None
    }

    processing_time = []
    stats_file = None
    analysis_list = None
    simulation_time = None

    def __init__(self, analysis_list, simulation_time):

        self.analysis_list = analysis_list
        self.simulation_time = simulation_time
        self.stats_file = open("client_stats.txt", "w")

        self.analysis_dict["average_time"] = self.get_average
        self.analysis_dict["maximum_time"] = self.get_max
        self.analysis_dict["minimum_time"] = self.get_min

    def get_average(self):

        self.stats_file.write(f"Average request processing time = "
                              + str(sum(self.processing_time) / len(self.processing_time)) + "\n")

    def get_max(self):

        self.stats_file.write(f"Maximum request processing time = "
                              + str(max(self.processing_time)) + "\n")

    def get_min(self):

        self.stats_file.write(f"Minimum request processing time = "
                              + str(min(self.processing_time)) + '\n')

    def start_analysis(self):

        time.sleep(self.simulation_time)

        for analy, val in self.analysis_list.items():
            if val == "yes":
                self.analysis_dict[analy]()

        self.stats_file.close()
        sys.exit(101)


class server_analysis():
    analysis_dict = {

        "no_of_clients_connected": None,
        "total_no_of_requests": None,
        "incoming_request_rate": None,
        "processing_rate": None
    }

    analysis_list = None
    simulation_time = None
    no_of_clients = 0
    no_of_requests = 0
    processed_requests = 0

    def __init__(self, analysis_list, simulation_time):

        self.analysis_list = analysis_list
        self.simulation_time = simulation_time
        self.stats_file = open("server_stats.txt", "w")

        self.analysis_dict["no_of_clients_connected"] = self.get_no_of_clients
        self.analysis_dict["total_no_of_requests"] = self.get_total_requests
        self.analysis_dict["incoming_request_rate"] = self.get_inrate
        self.analysis_dict["processing_rate"] = self.get_processing_rate

    def get_no_of_clients(self):

        self.stats_file.write(f"Number of clients connected      = "
                              + str(self.no_of_clients) + "\n")

    def get_total_requests(self):

        self.stats_file.write(f"Number of requests came          = "
                              + str(self.no_of_requests) + "\n")

    def get_inrate(self):

        self.stats_file.write(f"Incomming request rate           = "
                              + str(self.no_of_requests / self.simulation_time) + "\n")

    def get_processing_rate(self):
        self.stats_file.write(f"request processing rate          = "
                              + str(self.processed_requests / self.simulation_time) + "\n")

    def start_analysis(self):
        print("\nSimulation started.")

        for Time in range(self.simulation_time):
            sys.stdout.write("\rSimulation ends in %i " % (self.simulation_time - Time))
            sys.stdout.flush()
            time.sleep(1)
        print("\rFetching results....    ", end=" ")

        for analy, val in self.analysis_list.items():
            if val == "yes":
                self.analysis_dict[analy]()

        self.stats_file.close()
        time.sleep(0.5)
        print("\rSimulation ended.    ")
        sys.exit(101)
