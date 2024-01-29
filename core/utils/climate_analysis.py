import json
from os.path import join, dirname
from requests import get, RequestException
from locale_grabber import LocaleManager

class ClimateAnalyzer:
    """
    ClimateAnalyzer retrieves the current temperature in Kelvin for the user's city.
    """

    def __init__(self):
        """
        Initialize the ClimateAnalyzer instance.
        """
        self.config_path = join(dirname(__file__), '..', 'configs', 'locale.json')
        self.locale_manager = LocaleManager()

    def _get_temperature_from_config(self):
        """
        Retrieve the temperature from the config file.

        Returns:
            float: Temperature in Kelvin, or None if not found.
        """
        try:
            with open(self.config_path, 'r') as file:
                data = json.load(file)
                return data.get('temperature')
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def _fetch_temperature_from_api(self, latitude, longitude):
        """
        Fetch the current temperature from the Open-Meteo API for the given coordinates.

        Args:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.

        Returns:
            float: Current temperature in Kelvin, or None if the request fails.
        """
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"
            response = get(url)
            if response.status_code == 200:
                data = response.json()
                # Convert from Celsius to Kelvin
                temperature_celsius = data['current']['temperature_2m']
                return temperature_celsius + 273.15
            else:
                return None
        except RequestException:
            return None

    def get_temperature(self):
        """
        Get the current temperature in Kelvin for the user's location.

        Returns:
            float: Temperature in Kelvin, or None if unable to retrieve.
        """
        # Try to get temperature from config file
        temperature = self._get_temperature_from_config()
        if temperature is not None:
            return temperature

        # Use LocaleManager to retrieve location data
        user_info = self.locale_manager.global_retriever()
        if not user_info:
            return None

        latitude = user_info.get('lat')
        longitude = user_info.get('lon')
        if latitude is None or longitude is None:
            return None

        # Fetch temperature data from the Open-Meteo API
        return self._fetch_temperature_from_api(latitude, longitude)

# Example usage
if __name__ == "__main__":
    climate_analyzer = ClimateAnalyzer()
    temperature = climate_analyzer.get_temperature()
    print(f"Current Temperature: {temperature} K")
