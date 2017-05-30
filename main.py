import threading

from viewApp import carregarTela as carregarTela
from servidor import iniciarServidor as iniciarServidor
from updater import updateVersion as updateVersion

def iniciarAplicativo():
	servico = threading.Thread(target = iniciarServidor)
	app = threading.Thread(target = carregarTela)
	updater = threading.Thread(target = updateVersion)
	servico.start()
	app.start() 
	updater.start()


iniciarAplicativo()