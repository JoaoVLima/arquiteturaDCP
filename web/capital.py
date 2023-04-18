#!/usr/bin/env python3
import sys
import requests
from zeep import Client

class Capital:
    def __init__(self, country, url):
        self.country=country
        self.url = url

    def buscar_infos(self):
        cliente = Client(self.url + '?WSDL')

        response = cliente.service.CapitalCity(self.country)

        return response

if __name__ == "__main__":
    country = 'BR'
    if len(sys.argv) > 1:
        country = sys.argv[1]

    country_obj = Capital(country=country, url='http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso')

    print(country_obj.buscar_infos())
