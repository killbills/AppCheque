import threading

from viewApp import carregarTela as carregarTela
from servidor import iniciarServidor as iniciarServidor
from updater import Updater as updater

def iniciarAplicativo():
	servico = threading.Thread(target = iniciarServidor)
	app = threading.Thread(target = carregarTela)
	#updater = threading.Thread(target = updater)
	servico.start()
	app.start() 
	#updater.start()


iniciarAplicativo()