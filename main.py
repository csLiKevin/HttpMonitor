from argparse import ArgumentParser

from http_monitor import HttpMonitor


def run():
    """
    Driver function that grabs the command line arguments and starts the Http monitor.
    """
    argument_parser = ArgumentParser()
    argument_parser.add_argument("log_file", help="path to your log file")
    argument_parser.add_argument("-i", "--log_interval", default=10, help="how often summarize logs", type=float)
    argument_parser.add_argument("-w", "--log_window", default=120, help="time window for alerts", type=float)
    argument_parser.add_argument("-t", "--threshold", default=10, help="requests per second threshold", type=float)
    args = argument_parser.parse_args()

    log_file = args.log_file
    log_interval = args.log_interval
    log_window = args.log_window
    threshold = args.threshold

    monitor = HttpMonitor(log_file, threshold, log_interval, log_window)
    monitor.start()


if __name__ == "__main__":
    run()
