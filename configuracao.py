import os
import jsonpickle

caminhoArquivo = os.path.join(os.path.dirname(__file__), 'docs'+ os.sep +'configuracao.json')

class Configuracao:

	def __init__(self):
		self.urlSienge = None
		self.token = None
		self.matricial = self.ImpMatricial()
		self.cheque = self.ImpCheque()


	def parseFromJson(self, jsonValue):
		if jsonValue:
			self.__dict__ = jsonpickle.decode(jsonValue)
		else:
			self.__init__


	def carregar(self):
		with open(caminhoArquivo, 'r') as file:
			self.parseFromJson(file.read())


	def salvar(self):
		with open(caminhoArquivo, 'w') as file:
			print(jsonpickle.encode(self.__dict__))
			file.write(jsonpickle.encode(self.__dict__))


	class ImpMatricial:
		def __init__(self):
			self.porta = None
			self.outra = None


	class ImpCheque:
		def __init__(self):
			self.porta = None
			self.modelo = None
			self.outra = None
