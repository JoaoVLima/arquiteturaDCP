#!/usr/bin/env python3
import sys
import requests
from zeep import Client

class NumberConversion:
    def __init__(self, number, url):
        self.number=number
        self.url = url

    def buscar_infos(self):
        cliente = Client(self.url + '?WSDL')

        response = cliente.service.NumberToWords(self.number)

        return response

if __name__ == "__main__":
    number = 123
    if len(sys.argv) > 1:
        number = sys.argv[1]

    number_obj = NumberConversion(number=number, url='https://www.dataaccess.com/webservicesserver/NumberConversion.wso')

    print(number_obj.buscar_infos())
