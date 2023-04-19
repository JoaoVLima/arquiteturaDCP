from flask import Flask
from flask_restful import Resource, Api
import sys

app = Flask(__name__)
api = Api(app)

class Banco:
    def __init__(self, contas=None):
        if not contas:
            contas = {'1234-5': Conta('1234-5')}
        self.contas = contas

    def saldo(self, conta):
        conta_obj = self.contas.get(conta)
        if not conta_obj:
            raise 'Conta não existe'
        return conta_obj.saldo

    def deposito(self, conta, valor):
        conta_obj = self.contas.get(conta)
        if not conta_obj:
            raise 'Conta não existe'
        return conta_obj.deposito(valor)

    def saque(self, conta, valor):
        conta_obj = self.contas.get(conta)
        if not conta_obj:
            raise 'Conta não existe'
        return conta_obj.saque(valor)


class Conta:
    def __init__(self, codigo):
        self.codigo = codigo
        self.saldo = 0.0

    def deposito(self, valor):
        self.saldo += valor
        return self.saldo

    def saque(self, valor):
        if self.saldo < valor:
            raise 'Saldo Insuficiente'
        self.saldo -= valor
        return self.saldo



# URL	Resultado
# http://localhost:1512/contas/1234-5	para obter saldo da conta "1234-5"
# http://localhost:1512/contas/1234-5/deposito	para efetuar depósito de um valor na conta "1234-5"
# http://localhost:1512/contas/1234-5/saque	para efetuar o saque de um valor na conta "1234-5" (o saque pode produzir erro, se o saldo for insuficiente)

banco = Banco()

class SaldoIF(Resource):
    def get(self, conta):
        return banco.saldo(conta=conta)

class DepositoIF(Resource):
    def patch(self, conta):
        return banco.deposito(conta=conta, valor=1)

class SaqueIF(Resource):
    def patch(self, conta):
        return banco.saque(conta=conta, valor=1)


api.add_resource(SaldoIF, "/contas", "/contas/<string:conta>")
api.add_resource(DepositoIF, "/contas", "/contas/<string:conta>/deposito")
api.add_resource(SaqueIF, "/contas", "/contas/<string:conta>/saque")

if __name__ == '__main__':
    port = 1512
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.env = 'development'
    app.run(port=port, debug=True)
