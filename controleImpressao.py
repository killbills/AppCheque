import serial
import base64
import time
import logging
import sys  

from armanezamentoCheque import ArmanezamentoCheque
from configuracao import Configuracao
from printerException import ImpressoraSerialNaoConfiguradaException, ImpressoraMatricialNaoConfiguradaException, MatrizImpressaoCopiaException, MatrizImpressaoVersoException
from printers import PrinterFactory

class ControleImpressao:
    reload(sys)
    sys.setdefaultencoding('utf8')

    def __init__(self, ids):
        self.ids = ids
        self.configuracao = Configuracao()
        self.armazenamentoJsonCheques = ArmanezamentoCheque()
        self.armazenamentoJsonCheques.carregar()
        self.configuracao.carregar()


    def imprimirCheque(self):
        printerFactory = PrinterFactory()
        printer = printerFactory.getPrinter(self.configuracao)
        printer.printCheck(self.matrizImpressao)


    def imprimirMatricial(self):
        if self.configuracao.matricial['porta'] == 'OUTRA':
            porta = self.configuracao.matricial['outra']
        else:
            porta = self.configuracao.matricial['porta'] 
        
        logging.info('Abrindo porta ' + str(porta) + ' impressora matricial...')
        with open(porta, 'w') as par:
            logging.info(par)
            comando = base64.b64decode(self.matrizImpressao)
            par.write(comando)
            logging.info('Fechando porta ' + str(porta) + ' impressora matricial...')
            par.close()


    def imprimirCheques(self, copia, verso):
        self.validaConfiguracaoImpressora()

        cheque_list = self.armazenamentoJsonCheques.cheques
        cheques_sorted = sorted(cheque_list, key=lambda cheque_list: cheque_list['id'])

        for cheque in cheques_sorted:
            if cheque['id'] in self.ids:            
                self.validaMatrizImpressao(cheque, verso, copia)

                if cheque['tipoImpressora'] == "Matricial":
                    self.imprimirMatricial()
                else:
                    self.imprimirCheque()


    def validaMatrizImpressao(self, cheque, verso, copia):
        if copia == 'True':
            self.matrizImpressao = cheque['printMatrixCopia']
            if not self.matrizImpressao:
                raise MatrizImpressaoCopiaException(cheque['codigoContaCorrente'], cheque['numeroCheque'])
        elif verso == 'True':
            self.matrizImpressao = cheque['printMatrixVerso']
            if not self.matrizImpressao:
                raise MatrizImpressaoVersoException(cheque['codigoContaCorrente'], cheque['numeroCheque'])
        else:
            self.matrizImpressao = cheque['printMatrixCheque']


    def validaConfiguracaoImpressora(self):
        for cheque in self.armazenamentoJsonCheques.cheques:
            if cheque['id'] in self.ids:
                if cheque['tipoImpressora'] == "Matricial":
                    if not self.configuracao.matricial['porta']:
                        raise ImpressoraMatricialNaoConfiguradaException
                    if self.configuracao.matricial['porta'] == 'OUTRA' and not self.configuracao.matricial['outra']:
                        raise ImpressoraMatricialNaoConfiguradaException
                else:
                    if not self.configuracao.cheque['porta'] and not self.configuracao.cheque['modelo']:
                        raise ImpressoraSerialNaoConfiguradaException
                    if self.configuracao.cheque['porta'] == 'OUTRA' and not self.configuracao.cheque['outra']:
                        raise ImpressoraSerialNaoConfiguradaException