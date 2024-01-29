from json import load, JSONDecodeError
from os.path import join, dirname
from requests import get, RequestException
from locale import getlocale
from time import tzname
from datetime import datetime

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
        
    def global_retriever(self):
        """
        Retrieve global locale information based on the IP address using an external service.

        Returns:
            dict: A dictionary with various locale-related information or an empty dict in case of failure.
        """
        keys_to_omit = {'org', 'as', 'status'}

        try:
            response = get("http://ip-api.com/json/")
            if response.status_code == 200:
                result = response.json()
                return {k: v for k, v in result.items() if k not in keys_to_omit}
            else:
                return {}
        except RequestException:
            return {}
    
    def get_global_ip_locale(self):
        """
        Determine the estimated locale based on the global IP address.
        Returns the country code if successful. If unsuccessful, tries to infer from system language.
        If all else fails, returns 'XZ'.
        """
        global_info = self.global_retriever()
        country_code = global_info.get('countryCode', '')
        
        if country_code:
            return country_code

        # Fallback to the last two characters of the system language code
        system_language = self.get_system_locale_details().get('language', 'XX')
        return system_language[-2:].upper() if system_language else "XZ"
    
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
        current_locale = getlocale()
        time_zone = tzname[0]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "language": current_locale[0].upper() if current_locale and current_locale[0] else "XZ",
            "encoding": current_locale[1] if current_locale and current_locale[1] else "Unknown",
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