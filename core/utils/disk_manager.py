import logging
from ctypes import c_ulonglong, windll, c_wchar_p, byref
from sys import platform
from psutil import disk_usage
from cacheout import Cache
from time import sleep

class DiskManager:
    """
    DiskManager provides disk management and monitoring functionalities.
    It uses ctypes for Windows and psutil for Unix-like systems, with caching implemented via Cacheout.
    """
    def __init__(self):
        """
        Initialize the DiskManager instance.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('DiskManager')
        self.cache = Cache(maxsize=16, ttl=30)  # Cache with arbitrary values.

    def _fetch_disk_space(self, path):
        """
        Fetch disk space information for a specified path. Internal method to be called with caching.

        Args:
            path (str): Path for which disk space information is needed.

        Returns:
            dict: Disk space information.
        """
        if platform == "win32":
            return self._get_disk_space_windows(path)
        else:
            return self._get_disk_space_unix(path)

    def get_disk_space(self, path="."):
        """
        Get disk space information for a specified path with caching.

        Args:
            path (str): Path for which disk space information is needed. Default is the current directory.

        Returns:
            dict: Disk space information including total, used, and free space (in bytes).
        """
        cached_result = self.cache.get(path)
        if cached_result is not None:
            return cached_result

        result = self._fetch_disk_space(path)
        result_without_path = result.copy()
        result_without_path.pop("path", None) 

        self.cache.set(path, result_without_path)
        return result

    def _get_disk_space_windows(self, path):
        """
        Get disk space information on Windows using ctypes.

        Args:
            path (str): Path for which disk space information is needed.

        Returns:
            dict: Disk space information.
        """
        sleep(6)
        try:
            free_bytes = c_ulonglong()
            total_bytes = c_ulonglong()
            windll.kernel32.GetDiskFreeSpaceExW(
                c_wchar_p(path),
                byref(free_bytes),
                byref(total_bytes),
                None
            )

            total_space = total_bytes.value
            free_space = free_bytes.value
            used_space = total_space - free_space
                       
            return {
                "path": path,
                "total_space_bytes": total_space,
                "used_space_bytes": used_space,
                "free_space_bytes": free_space
            }
        except Exception as e:
            self.logger.error(f"Error getting disk space on Windows: {e}")
            return {"error": str(e)}

    def _get_disk_space_unix(self, path):
        """
        Get disk space information on Unix-like systems using psutil.

        Args:
            path (str): Path for which disk space information is needed.

        Returns:
            dict: Disk space information.
        """
        try:
            usage = disk_usage(path)
            return {
                "path": path,
                "total_space_bytes": usage.total,
                "used_space_bytes": usage.used,
                "free_space_bytes": usage.free
            }
        except Exception as e:
            self.logger.error(f"Error getting disk space on Unix: {e}")
            return {"error": str(e)}

# Additional methods for disk management will be added here.
if __name__ == "__main__":
    disk_manager = DiskManager()
    result = disk_manager.get_disk_space()
    print(result)
    