import requests


def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Để lấy thông tin thời tiết dưới đơn vị Celsius
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            print(
                f"Failed to retrieve weather data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def display_weather(weather_data):
    if weather_data:
        main = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        print(f"Thời tiết hiện tại: {main} - {description}")
        print(f"Nhiệt độ hiện tại: {temp}°C")
    else:
        print("Không thể lấy thông tin thời tiết.")


# Thay thế 'YOUR_API_KEY' bằng API Key của bạn từ OpenWeatherMap
api_key = '3006163953351dc1f62128a042658400'
city = 'Hanoi'  # Thay thế thành tên thành phố bạn muốn xem thông tin thời tiết

weather_data = get_weather(api_key, city)
display_weather(weather_data)
