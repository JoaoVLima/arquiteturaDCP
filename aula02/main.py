#!/usr/bin/env python3

import sys
import os
import ast
import etcd3


class Conexao:
    def __init__(self):
        self.etcd = etcd3.client(host='localhost', port=2379)


class Cliente(Conexao):
    def __init__(self, nome: str):
        super().__init__()
        self.nome = nome

    def get(self, key, prefix: bool = False, is_return_dict: bool = False):
        if prefix:
            value, metadata = self.etcd.get_prefix(key_prefix=str(key))
        else:
            value, metadata = self.etcd.get(key=str(key))

        value = value.decode('utf-8')
        metadata = metadata.key.decode('utf-8')

        if is_return_dict:
            value = ast.literal_eval(value)

        return value

    def put(self, key, value):
        try:
            self.etcd.put(key=str(key), value=str(value))
        except:
            return False
        return True


if __name__ == "__main__":
    nome_cliente = 'candidatoA'
    if len(sys.argv) > 1:
        nome_cliente = sys.argv[1]

    cliente = Cliente(nome=nome_cliente)
    cliente.put('teste', 'valor')
    cliente.put('teste2', {'lider': 'A'})
    teste = cliente.get('teste')
    teste2 = cliente.get('teste2', is_return_dict=True)

    print(teste, teste2)
