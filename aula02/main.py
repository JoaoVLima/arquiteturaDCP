#!/usr/bin/env python3

import sys
import os


def servidor():
    pass


def cliente():
    pass




if __name__ == "__main__":
    tipo = 'servidor'
    if len(sys.argv) > 1:
        tipo = sys.argv[1]

    if tipo == 'servidor':
        servidor()
    elif tipo == 'cliente':
        cliente()
