#!/usr/bin/env python3

import sys
import os
import random
import uuid


class Comunicacao:
    def __init__(self, write_fifo=None, read_fifo=None):
        self.write_fifo = write_fifo
        self.read_fifo = read_fifo

    def criar_canal(self, nome):
        os.mkfifo(nome)

    def remover_canal(self, nome):
        os.unlink(nome)

    def ler_canal(self):
        pass

    def escrever_canal(self):
        pass

class Servidor(Comunicacao):
    def __init__(self, write_fifo, read_fifo):
        super().__init__(write_fifo=write_fifo, read_fifo=read_fifo)
        self.ler_canal(read_fifo)
        self.remover_canal(read_fifo)

    def gerar_id(self):
        return random.randint(1, 1000)

    def ler_canal(self, nome):
        e = os.open(nome, os.O_RDONLY)
        msg = os.read(e, 128).decode('utf-8')

        print(f'Recebido: "{msg}"')


class Cliente(Comunicacao):
    def __init__(self, write_fifo, read_fifo):
        super().__init__(write_fifo=write_fifo, read_fifo=read_fifo)
        self.escrever_canal(write_fifo)

    def escrever_canal(self, nome):
        e = os.open(nome, os.O_WRONLY)
        os.write(e, b'oi')


if __name__ == "__main__":
    tipo = 'servidor'
    if len(sys.argv) > 1:
        tipo = sys.argv[1]

    if tipo == 'servidor':
        Servidor(write_fifo='', read_fifo='canal')
    elif tipo == 'cliente':
        Cliente(write_fifo='canal', read_fifo='')
