#!/usr/bin/env python3
import sys
import requests

class Weather:
    def __init__(self, city, url):
        self.city=city
        self.url = url

    def buscar_infos(self):
        params = {
            'q': self.city,
            'appid': '442de31b43491aba83051131ecfeffe3'
        }

        response = requests.get(url=self.url, params=params).json()

        return response

if __name__ == "__main__":
    city = 'Curitiba'
    if len(sys.argv) > 1:
        city = sys.argv[1]

    city_obj = Weather(city=city, url='http://api.openweathermap.org/data/2.5/weather')

    print(city_obj.buscar_infos())
