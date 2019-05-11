from unittest import TestCase
from unittest.mock import patch

from http_monitor import HttpMonitor


class TestHttpMonitor(TestCase):
    @patch('time.sleep', side_effect=lambda x: x)
    def test_high_traffic_triggered(self, sleep_mock):
        http_monitor = HttpMonitor("./data/test.csv", 0, 1, 1)
        http_monitor.start()
        self.assertTrue(http_monitor.high_traffic)

    @patch('time.sleep', side_effect=lambda x: x)
    def test_high_traffic_recovered(self, sleep_mock):
        http_monitor = HttpMonitor("./data/test.csv", 5, 1, 1)
        http_monitor.high_traffic = True
        http_monitor.start()
        self.assertFalse(http_monitor.high_traffic)
