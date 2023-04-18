#!/usr/bin/env python3
import sys
import subprocess
import xmltodict

class Curl:
    def __init__(self, flags:str='', url:str=''):
        self.command = 'curl'
        self.flags = flags
        self.url = url

    def append_flags(self, flags):
        if self.flags:
            self.flags += ' ' + flags
        else:
            self.flags = flags

    def execute(self):
        response = subprocess.check_output([self.command, self.flags, self.url])
        return response

    def get(self, url:str=None, params:dict=None):
        flags = '-sS'
        self.append_flags(flags)

        if url:
            self.url = url

        if params:
            params_str = self.dict_to_str(params)
            self.url += f'?{params_str}'

        return self.execute()


    def post(self, url:str=None, params:dict=None):
        flags = '-sS -X POST'
        self.append_flags(flags)

        if url:
            self.url = url

        if params:
            params_str = self.dict_to_str(params)
            flags = f"-d '{params_str}'"
            self.append_flags(flags)

        return self.execute()

    def dict_to_str(self, dictionary:dict):
        string = ''
        for k, v in dictionary.items():
            string += f'{k}={v}'

        return string

class Cep(Curl):
    def __init__(self, cep, **kwargs):
        super().__init__(**kwargs)
        self.cep=cep

    def buscar_infos(self):
        params = {
            'cep': self.cep
        }
        response = self.get(params=params)

        resonse_parsed = xmltodict.parse(response)

        resonse_parsed = resonse_parsed['webservicecep']

        resonse_parsed.pop('resultado')
        resonse_parsed.pop('resultado_txt')

        return resonse_parsed



if __name__ == "__main__":
    cep = '80215901'
    if len(sys.argv) > 1:
        cep = sys.argv[1]

    cep_obj = Cep(cep=cep, url='http://cep.republicavirtual.com.br/web_cep.php')

    print(cep_obj.buscar_infos())
