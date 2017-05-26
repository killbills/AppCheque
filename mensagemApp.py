import json


class mensagemApp:
	def __init__(self, status, titulo, mensagem):
		self.titulo = titulo
		self.status = status
		self.mensagem = mensagem


	def toJSON(self):
		return json.loads(json.dumps(self, default = lambda o: o.__dict__, sort_keys=True, indent=4))


def sucesso(mensagem):
	return mensagemApp('sucesso' , 'Sucesso!', mensagem).toJSON()


def falha(mensagem):
	return mensagemApp('alerta' , 'Ops! Algo deu errado...', mensagem).toJSON()
