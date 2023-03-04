from datetime import datetime
import requests
from .app import MAPBOX_KEY, WEATHER_API

def get_coordinates(location):
    """Helper function for Geocoding, with Mapbox API

    Args:
        location (string): Pass in location as string to the url 
        'https://api.mapbox.com/geocoding/v5/mapbox.places/<location>.json?access_token=<mapbox_token>'

    Returns:
        list: returns latitude and longitude coordinates, i.e [-20054, 33625]
    """
    response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={MAPBOX_KEY}')
    data = response.json()
    coordinates = data['features'][0]['center']
    
    return coordinates


def get_forecast(lat, lon, period, location):
    """Helper function to get weather data with Openweathermap API

    Args:
        lat (float): Latitude received from geocoding api
        lon (float): Longitude received from geocoding api
        location (string): Address/Location for the request

    Returns:
        dict: Transformed data from response saved into a dictionary.
    """
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt={period}&mode=json&units=metric&appid={WEATHER_API}&exclude=hourly' 
    data = requests.get(url).json()
    

    # Store necessary data from response in a dictionary
    forecast_data = {
            'location': location,
            'period': period,
            'forecast': [
                {
                'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                'max': item['main']["temp_max"],
                'min': item['main']["temp_min"],
                'humidity': item['main']['humidity'],
                } for item in data['list']
            ],
    }
    
    return forecast_data
    