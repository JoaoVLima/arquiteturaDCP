from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
class Eco:
    def __init__(self, sufixo):
        self.sufixo = sufixo
        self.cont = 0

    def diga(self, msg):
        self.cont += 1
        return msg + self.sufixo



eco = Eco('_ECO')
class EcoIF(Resource):
    def get(self):
        return {'cont': eco.cont}

    def patch(self, msg):
        return {'resp': eco.diga(msg)}


api.add_resource(EcoIF, "/eco", "/eco/<string:msg>")

if __name__ == '__main__':
    app.env = 'development'
    app.run(port=1512, debug=True)
