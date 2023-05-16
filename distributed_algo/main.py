#!/usr/bin/env python3

from sys import argv
from pika import BlockingConnection

class Componente:
    def __init__(self, identificador:str, lista_vizinhos:list):
        self.identificador = identificador
        self.lista_vizinhos = lista_vizinhos

        self.conexao = BlockingConnection()
        self.canal = self.conexao.channel()

        self.mensagens_recebidas = []

        self.criar_filas()

        self.aguardar_mensagem(callback=self.recebendo)

    def criar_filas(self):
        print(f'Criando as filas {self.identificador} e {self.lista_vizinhos}')
        self.canal.queue_declare(queue=self.identificador, auto_delete=True)

        for vizinho in self.lista_vizinhos:
            self.canal.queue_declare(queue=vizinho, auto_delete=True)

    def aguardar_mensagem(self, callback):
        print(f'Aguardando Mensagem no {self.identificador}')
        self.canal.basic_consume(queue=self.identificador, on_message_callback=callback, auto_ack=True)

        try:
            self.canal.start_consuming()
        except KeyboardInterrupt as e:
            self.canal.stop_consuming()

    def enviar_mensagem(self, vizinho, mensagem):
        print(f'Enviando mensagem "{mensagem}" para {vizinho}')
        self.canal.basic_publish(exchange="", routing_key=vizinho, body=mensagem)

    def espalhar_mensagem(self, mensagem, fofocador=None):
        lista_vizinhos = self.lista_vizinhos[:]

        if fofocador and fofocador in lista_vizinhos:
            lista_vizinhos.remove(fofocador)

        mensagem_composta = f'{self.identificador}:{mensagem}'

        for vizinho in lista_vizinhos:
            self.enviar_mensagem(vizinho=vizinho, mensagem=mensagem_composta.encode())

        self.mensagens_recebidas.append(mensagem_composta)

    def recebendo(self, ch, method, properties, body):  #Recebendo
        mensagem_composta = body.decode()
        mensagem_composta_split = mensagem_composta.split(':', maxsplit=1)

        if len(mensagem_composta_split) < 2:
            fofocador = 'NULL'
            mensagem = mensagem_composta_split[0]
        else:
            fofocador, mensagem = mensagem_composta_split

        print(f'Recebendo mensagem "{mensagem}" do {fofocador}')

        if mensagem_composta in self.mensagens_recebidas:
            print(f'Mensagem já enviada anteriormente: {mensagem_composta}')
        else:
            self.espalhar_mensagem(fofocador=fofocador, mensagem=mensagem)



if __name__ == "__main__":
    idx = '0'
    Nx = []
    if len(argv) > 1:
        idx = argv[1]
        Nx = argv[2:]

    componente = Componente(identificador=idx, lista_vizinhos=Nx)

