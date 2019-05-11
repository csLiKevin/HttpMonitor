from csv import DictReader

from utils import print_info


class HttpMonitor(object):
    """
    Class responsible for reading a log file and printing information about it as it processes through it.
    """

    def __init__(self, log_file, threshold):
        """
        Constructor
        :param log_file: Path to a log file.
        :param threshold: Requests per second considered to be high traffic.
        """
        self.log_file = log_file
        self.threshold = threshold

    @classmethod
    def read_logs(cls, reader, seconds=10):
        """
        Read lines until the specified number of seconds has passed.

        :param reader: DictReader wrapper containing a csv file.
        :param seconds: Number of seconds to read the log file for.
        :return: A summary of the logs that were read.
        """

        line = next(reader)
        start_time = int(line["date"])
        current_time = start_time

        while current_time - start_time < seconds:
            line = next(reader)
            current_time = int(line["date"])

    def start(self):
        """
        Start processing the log file.
        """
        print_info(f"Start monitoring {self.log_file}")
        with open(self.log_file) as log_file:
            reader = DictReader(log_file)
            self.read_logs(reader)
