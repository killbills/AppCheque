import serial
import base64
import time
import logging

from abc import ABCMeta, abstractmethod
from printerException import ErroImpressoraException

class ImpressoraCheque(object):
    __metaclass__ = ABCMeta

    def __init__(self, porta):
        logging.info('Configurando porta serial...')
        self.serial = serial.Serial()
        self.serial.port = porta
        pass

    @abstractmethod
    def serialSetup():
        pass

    @abstractmethod
    def printCheck(self, matrizCheque):
        logging.info('Iniciando impressao cheque...')
        self.serial.open()
        pass

class PrinterFactory:

    def __init__(self):
        pass

    def getPrinter(self, configuracao):
        modelo = configuracao.cheque['modelo']

        if configuracao.cheque['porta'] == 'OUTRA':
            porta = configuracao.cheque['outra']
        else:
            porta = configuracao.cheque['porta']
 
        logging.info('Impressora ' + str(modelo) + ' na porta ' + str(porta))

        if modelo == 'Bematech':
            printer = Bematech(porta)
        if modelo == 'ImpreCheq':
            printer = ImpreCheq(porta)
        if modelo == 'CheckPronto':
            printer = CheckPronto(porta)
        if modelo == 'FastCheck':
            printer = FastCheck(porta)
        if modelo == 'PratikCheque':
            printer = PratikCheque(porta)
        if modelo == 'Elgin':
            printer = Elgin(porta)
        if modelo == 'EasyAp40N':
            printer = EasyAp40N(porta)
        if modelo == 'PertoCheck':
            printer = PertoCheck(porta)

        printer.serialSetup()

        return printer

class Bematech(ImpressoraCheque):
    
    def serialSetup(self):    
        self.serial.baudrate = 9600
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.bytesize = serial.EIGHTBITS
        logging.info(self.serial)

    def printCheck(self, matrizCheque):
        super(Bematech, self).printCheck(matrizCheque)
        if self.serial.is_open:
            self.serial.write(base64.b64decode(matrizCheque))
            time.sleep(.3)
            self.serial.flushOutput()
            self.serial.close()
        else:
            raise ErroImpressoraException


class ImpreCheq(ImpressoraCheque):

    def serialSetup(self):
        self.serial.baudrate = 9600
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_TWO
        self.serial.bytesize = serial.EIGHTBITS
        logging.info(serial)

    def printCheck(self, matrizCheque):
        super(ImpreCheq, self).printCheck(matrizCheque)
        if self.serial.is_open:
            comando = base64.b64decode(matrizCheque).encode('hex') + '\f'.encode('hex')
            self.serial.write(comando)
            time.sleep(.3)
            self.serial.flushOutput()
            self.serial.close()
        else:
            raise ErroImpressoraException


class CheckPronto(ImpressoraCheque):
    
    def serialSetup(self):
        self.serial.baudrate = 9600
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.bytesize = serial.EIGHTBITS
        logging.info(self.serial)

    def printCheck(self, matrizCheque):
        super(CheckPronto, self).printCheck(matrizCheque)
        if self.serial.is_open:
            self.serial.write(base64.b64decode(matrizCheque))
            time.sleep(.3)
            self.serial.flushOutput()
            self.serial.close()
        else:
            raise ErroImpressoraException


class FastCheck(ImpressoraCheque):
    
    def serialSetup(self):
        self.serial.baudrate = 9600
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_TWO
        self.serial.bytesize = serial.EIGHTBITS
        logging.info(self.serial)

    def printCheck(self, matrizCheque):
        super(FastCheck, self).printCheck(matrizCheque)
        if self.serial.is_open:
            self.serial.write(base64.b64decode(matrizCheque))
            time.sleep(.3)
            self.serial.flushOutput()
            self.serial.close()
        else:
            raise ErroImpressoraException


class PratikCheque(ImpressoraCheque):
    
    def serialSetup(self):
        self.serial.baudrate = 9600
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_TWO
        self.serial.bytesize = serial.EIGHTBITS
        logging.info(self.serial)

    def printCheck(self, matrizCheque):
        super(PratikCheque, self).printCheck(matrizCheque)
        if self.serial.is_open:
            self.serial.write(base64.b64decode(matrizCheque))
            time.sleep(.3)
            self.serial.flushOutput()
            self.serial.close()


class Elgin(ImpressoraCheque):
    
    def serialSetup(self):
        self.serial.baudrate = 9600
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_TWO
        self.serial.bytesize = serial.EIGHTBITS
        logging.info(self.serial)

    def printCheck(self, matrizCheque):
        super(Elgin, self).printCheck(matrizCheque)
        if self.serial.is_open:
            self.serial.write(base64.b64decode(matrizCheque))
            time.sleep(.3)
            self.serial.flushOutput()
            self.serial.close()
        else:
            raise ErroImpressoraException


class EasyAp40N(ImpressoraCheque):
    
    def serialSetup(self):
        self.serial.baudrate = 9600
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_TWO
        self.serial.bytesize = serial.EIGHTBITS
        logging.info(self.serial)

    def printCheck(self, matrizCheque):
        super(EasyAp40N, self).printCheck(matrizCheque)
        if self.serial.is_open:
            self.serial.write(base64.b64decode(matrizCheque))
            time.sleep(.3)
            self.serial.flushOutput()
            self.serial.close()
        else:
            raise ErroImpressoraException

class PertoCheck(ImpressoraCheque):

    def serialSetup(self):
        self.serial.baudrate = 4800
        logging.info(self.serial)

    def printCheck(self, matrizCheque):
        super(PertoCheck, self).printCheck(matrizCheque)
        if self.serial.is_open:
            decodedMatrix = base64.b64decode(matrizCheque).encode('UTF-8')
            self.serial.write(self.montaMensagem('='))
            self.readPertoCheck(45)
            time.sleep(.5)
            self.sendACK()
            for comando in decodedMatrix.split('\n'):
                if not comando == '':
                    comando = comando.replace('$', ';')
                    self.serial.write(self.montaMensagem(comando))
                    self.readPertoCheck(3)
                    time.sleep(.5)
                    self.sendACK()
            self.serial.close()
        else:
            raise ErroImpressoraException        


    def montaMensagem(self, comando):
        stx = '\x02'
        etx = '\x03'
        bcc = ord(stx)

        for c in comando:
            bcc = bcc ^ ord(c)

        bcc = bcc ^ ord(etx)

        mensagem = stx + comando + etx + chr(bcc)
        return mensagem.encode()

    
    def readPertoCheck(self, timeout):
        self.serial.timeout = timeout
        res = self.serial.read_until('\x03')
        stop = False
        while (stop):
            resBcc = self.serial.read_until()
            if not resBcc == res:
                stop = True
        return res

    
    def sendACK(self):
        self.serial.write('6'.encode())

    
    def sendNACK(self):
        self.serial.write('21'.encode())