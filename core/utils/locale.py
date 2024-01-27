from json import load, JSONDecodeError
from os.path import join, dirname
from requests import get, RequestException
from locale import getdefaultlocale
from time import tzname
from datetime import datetime

# Comment: WHY ISN'T IT WORKING?! WHAT

class LocaleManager:
    """
    LocaleManager handles the detection and retrieval of locale-related information.
    It combines system-specific details, user preferences, and global IP-based locale estimation.
    """
    
    def __init__(self):
        """
        Initialize the LocaleManager instance.
        """
        self.config_path = join(dirname(__file__), '..', 'configs', 'locale.json')
    
    def get_global_ip_locale(self):
        """
        Determine the estimated locale based on the global IP address using an external service.
        Returns the country code if successful, 'Unknown' otherwise.
        """
        try:
            response = get("http://ip-api.com/json/") # Needs to be configured. Not working yet.
            return response.json().get('countryCode', 'Unknown')
        except RequestException:
            return "Unknown"
    
    def get_preferred_locale(self):
        """
        Retrieve the preferred locale settings from a configuration file.
        Returns the contents of the locale.json file or None if the file is not found or invalid.
        """ # The config file will be created and saved by some manager, outside of this script.
        try:
            with open(self.config_path, 'r') as file:
                return load(file)
        except (FileNotFoundError, JSONDecodeError):
            return None
    
    def get_system_locale_details(self):
        """
        Gather system-specific locale details like language, encoding, time zone, and current time.
        Returns a dictionary with these details.
        """
        current_locale = getdefaultlocale()
        time_zone = tzname[0]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        return {
            "language": current_locale[0] if current_locale else "Unknown",
            "encoding": current_locale[1] if current_locale else "Unknown",
            "time_zone": time_zone,
            "current_time": current_time
        }
    
    
    def get_locale(self):
        """
        Attempts to retrieve the preferred user locale from the configuration file first.
        If not available, it combines system locale details and global IP-based locale.
        Returns a comprehensive dictionary of the locale information.
        """
        preferred_locale = self.get_preferred_locale()
        if preferred_locale:
            return preferred_locale
    
        global_ip_locale = self.get_global_ip_locale()
        system_locale_details = self.get_system_locale_details()
    
        return {
            "global_ip_locale": global_ip_locale,
            "system_locale": system_locale_details
        }

if __name__ == "__main__":
    locale_manager = LocaleManager()
    locale_info = locale_manager.get_locale()
    print(locale_info)

"""
Typical type of output and input:
{
    "global_ip_locale": "US",
    "system_locale": {
        "language": "en_US",  # or similar
        "encoding": "UTF-8",  # or similar
        "time_zone": "Eastern",  # or "EDT", depending on the date and time
        "current_time": "2024-01-27 15:45:00"  # example current time
    }
}
"""