#!/usr/bin/env python3

import sys
import os
import random
import uuid


# class Comunicacao:
#     def __init__(self, write_fifo=None, read_fifo=None):
#         self.write_fifo = write_fifo
#         self.read_fifo = read_fifo
#
#     def criar_canal(self, filename):
#         os.mkfifo(filename)
#
#     def remover_canal(self, filename):
#         os.unlink(filename)
#
#     def ler_canal(self, filename):
#         pass
#
#     def escrever_canal(self, filename, msg):
#         pass
#
# class Servidor(Comunicacao):
#     def __init__(self, write_fifo, read_fifo):
#         super().__init__(write_fifo=write_fifo, read_fifo=read_fifo)
#         self.criar_canal(self.read_fifo)
#         self.ler_canal(self.read_fifo)
#         self.remover_canal(self.read_fifo)
#
#     def gerar_id(self):
#         return random.randint(1, 1000)
#
#     def ler_canal(self, filename):
#         e = os.open(filename, os.O_RDONLY)
#         msg = os.read(e, 128).decode('utf-8')
#
#         print(f'Recebido: "{msg}"')
#
#         self.criar_canal(filename=msg)
#
#
# class Cliente(Comunicacao):
#     def __init__(self, write_fifo, read_fifo):
#         super().__init__(write_fifo=write_fifo, read_fifo=read_fifo)
#         self.escrever_canal(write_fifo, b'oi')
#         self.ler_canal(read_fifo)
#
#     def escrever_canal(self, filename, msg):
#         e = os.open(filename, os.O_WRONLY)
#         os.write(e, msg)
#
#     def ler_canal(self, filename):
#         e = os.open(filename, os.O_RDONLY)
#         msg = os.read(e, 128).decode('utf-8')
#
#         print(f'Recebido: "{msg}"')
#


def gerar_id():
    return random.randint(1, 1000)


def servidor():
    os.mkfifo('canal')
    e = os.open('canal', os.O_RDONLY)
    msg = os.read(e, 128).decode('utf-8')

    print(f'Recebido: "{msg}"')

    os.mkfifo(msg)

    e = os.open(msg, os.O_WRONLY)
    os.write(e, bytes(str(gerar_id()), 'utf-8'))



def cliente():
    e = os.open('canal', os.O_WRONLY)
    os.write(e, bytes('c1', 'utf-8'))

    a = os.open('c1', os.O_RDONLY)

    msg = os.read(a, 128).decode('utf-8')

    print(f'Recebido: "{msg}"')




if __name__ == "__main__":
    tipo = 'servidor'
    if len(sys.argv) > 1:
        tipo = sys.argv[1]

    if tipo == 'servidor':
        servidor()
    elif tipo == 'cliente':
        cliente()
