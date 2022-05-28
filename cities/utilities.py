import requests
import time
from Django_Internship_2022.config import open_weather_key
import tempfile
from PIL import Image


def duration(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        print('Execution time: ', round(time.time() - start, 3))
        return return_value
    return wrapper


def get_weather(city_name, country_code):
    api_link = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_key}'
    response = requests.get(api_link, params={'units': 'metric'})
    json_response = response.json()
    if json_response['cod'] == 200:
        icon = json_response['weather'][0]['icon']
        weather = {
            'description': json_response['weather'][0]['description'],
            'icon': f"https://openweathermap.org/img/wn/{icon}@2x.png",
            'temperature': json_response['main']['temp'],
            'feels_like': json_response['main']['feels_like'],
            'pressure': json_response['main']['pressure'],
            'humidity': json_response['main']['humidity'],
            'wind_speed': json_response['wind']['speed']
        }
        return weather
    else:
        return dict()


def temporary_image():
    """
    Returns a new temporary image file
    """
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)  # important because after save(), the fp is already at the end of the file
    return tmp_file
