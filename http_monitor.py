from collections import defaultdict
from csv import DictReader
from time import sleep

from utils import print_info, print_warning, print_error, print_success


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
    def read_logs(cls, reader, seconds=10):
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

            high_traffic = False
            # Keep track of the number of requests in the last two minutes.
            request_counts = []
            while True:
                try:
                    timestamp, average_bytes, most_hit_section, count = self.read_logs(reader)
                    print_info(f"{timestamp}\t{average_bytes:.2f}\t{most_hit_section}")

                    request_counts.append(count)
                    # Only keep the last 12 counts because each count represents 10 seconds.
                    request_counts = request_counts[-12:]
                    requests_per_second = sum(request_counts) / 120

                    # Check if the requests per second has exceeded or recovered from the traffic threshold.
                    if requests_per_second >= self.threshold and high_traffic is False:
                        print_error("High traffic detected.")
                        high_traffic = True
                    elif requests_per_second < self.threshold and high_traffic is True:
                        print_success("Traffic has stabilized.")
                        high_traffic = False

                    # Simulate 10 seconds of time passing. DO NOT USE for real access logs.
                    sleep(10)
                except StopIteration:
                    print_warning("End of file has been reached.")
                    exit()
