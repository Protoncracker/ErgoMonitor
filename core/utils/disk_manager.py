import ctypes
import logging
from ctypes import wintypes

class DiskManager:
    """
    DiskManager provides functionalities for disk management and monitoring.
    """

    def __init__(self):
        """
        Initialize the DiskManager instance.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('DiskManager')

    def get_disk_space(self, path="."):
        """
        Get disk space information for a specified path using ctypes to call the Windows API.

        Args:
            path (str): Path for which disk space information is needed. Default is the current directory.

        Returns:
            dict: Disk space information including total, used, and free space (in bytes).
        """
        try:
            free_bytes = wintypes.ULONGlong()
            total_bytes = wintypes.ULONGlong()
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                path,
                ctypes.byref(free_bytes),
                ctypes.byref(total_bytes),
                None
            )

            total_space = total_bytes.value
            free_space = free_bytes.value
            used_space = total_space - free_space

            return {
                "path": path,
                "total_space": total_space,
                "used_space": used_space,
                "free_space": free_space
            }
        except Exception as e:
                self.logger.error(f"Error getting disk space: {e}")
                return {}

    # Additional methods for disk management can be added here.