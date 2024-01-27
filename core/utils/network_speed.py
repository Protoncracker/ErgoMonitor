import speedtest
import logging

class NetworkSpeed:
    """
    NetworkSpeed measures the network download and upload speeds, as well as ping,
    and returns the results as raw data.
    """

    def __init__(self):
        """
        Initialize the NetworkSpeed instance.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('NetworkSpeed')
        self.speed_test = speedtest.Speedtest()

    def test_speed(self):
        """
        Test and return the network download and upload speeds and ping.

        Returns:
            dict: Dictionary containing download, upload speeds (in Mbps) and ping (in ms).
            Or
            str: Error message if an error occurs.
        """
        try:
            download_speed = round(self.speed_test.download() / 1_000_000, 2)  # Convert to Mbps
            upload_speed = round(self.speed_test.upload() / 1_000_000, 2)  # Convert to Mbps
            ping = self.speed_test.results.ping

            return {
                "download_speed_mbps": download_speed,
                "upload_speed_mbps": upload_speed,
                "ping_ms": ping
            }
        except Exception as e:
            self.logger.error(f"Error during speed test: {e}")
            return f"Error during speed test: {e}"

if __name__ == "__main__":
    network_speed = NetworkSpeed()
    test_results = network_speed.test_speed()
    if isinstance(test_results, str):
        logging.error(test_results)
    else:
        logging.info(f"Speed Test Results: {test_results}")
