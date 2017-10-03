import os
import jsonpickle


caminhoArquivo = os.path.join(
    os.path.dirname(__file__), 'docs'+ os.sep +'cheques.json')


class ArmanezamentoCheque:

    def __init__(self, jsonValue = None):
        self.jsonValue = jsonValue
        self.cheques = []


    def carregar(self):
        with open(caminhoArquivo, 'r') as file:
             self.__dict__ = jsonpickle.decode(file.read())


    def salvar(self):            
        with open(caminhoArquivo, 'w') as file:
            file.write(jsonpickle.encode(self.jsonValue))