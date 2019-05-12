from collections import defaultdict
from csv import DictReader
import time

from utils import print_info, print_warning, print_error, print_success


class HttpMonitor(object):
    """
    Class responsible for reading a log file and printing information about it as it processes through it.
    """

    def __init__(self, log_file, threshold, log_interval, log_window):
        """
        Constructor

        :param log_file: Path to a log file.
        :param threshold: Requests per second considered to be high traffic.
        :param log_interval: Number of seconds to collect logs before printing a summary.
        :param log_window: Number of seconds to look back when checking for high traffic.
        """
        self.log_file = log_file
        self.log_interval = log_interval
        self.log_window = log_window
        self.threshold = threshold
        self.high_traffic = False

    @classmethod
    def get_request_section(cls, request):
        """
        Get the section of a request. A section is defined as being the characters before the second /.

        :param request: String summarizing a request.
        :return: The section of a resource.
        """
        request_type, resource, protocol = request.split(" ")
        section = resource.split("/")[1]
        return f"/{section}"

    @classmethod
    def read_logs(cls, reader, seconds):
        """
        Read lines until the specified number of seconds has passed.

        :param reader: DictReader wrapper containing a csv file.
        :param seconds: Number of seconds to read the log file for.
        :return: A summary of the logs that were read.
        """
        average_bytes = 0
        sections = defaultdict(int)

        line = next(reader)
        current_time = int(line["date"])
        average_bytes += int(line["bytes"])
        section = cls.get_request_section(line["request"])
        sections[section] += 1

        start_time = current_time
        count = 1

        # Read logs until the time exceeds specified number of seconds has passed.
        while current_time - start_time < seconds:
            line = next(reader)
            current_time = int(line["date"])
            average_bytes += int(line["bytes"])
            section = cls.get_request_section(line["request"])
            sections[section] += 1
            count += 1

        average_bytes /= count
        most_hit_section = max(sections.keys(), key=lambda key: sections[key])

        return current_time, average_bytes, most_hit_section, count

    def start(self):
        """
        Start processing the log file.
        """
        print_info(f"Start monitoring {self.log_file}")
        with open(self.log_file) as log_file:
            reader = DictReader(log_file)

            # Keep track of the number of requests in the log window.
            request_counts = []
            while True:
                try:
                    timestamp, average_bytes, most_hit_section, count = self.read_logs(reader, self.log_interval)
                    print_info(f"{timestamp}\t{average_bytes:.2f}\t{most_hit_section}")

                    request_counts.append(count)
                    # Only keep enough counts to cover the time in the log window.
                    request_counts = request_counts[-(self.log_window // self.log_interval):]
                    requests_per_second = sum(request_counts) / self.log_window

                    # Check if the requests per second has exceeded or recovered from the traffic threshold.
                    if requests_per_second >= self.threshold and self.high_traffic is False:
                        print_error(f"High traffic generated an alert - hits = {requests_per_second:.2f} requests per "
                                    f"second, triggered at {timestamp}")
                        self.high_traffic = True
                    elif requests_per_second < self.threshold and self.high_traffic is True:
                        print_success(f"Traffic has stabilized - hits = {requests_per_second:.2f} requests per second, "
                                      f"recovered at {timestamp}")
                        self.high_traffic = False

                    # Simulate time passing. DO NOT USE for real access logs.
                    time.sleep(self.log_interval)
                except StopIteration:
                    print_warning("End of file has been reached.")
                    break
