class ImpressoraSerialNaoConfiguradaException(Exception):
    def __init__(self):
        self.mensagem = 'A impressora de cheque nao esta habilitada. Verifique as configuracoes e tente novamente.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem


class ImpressoraMatricialNaoConfiguradaException(Exception):
    def __init__(self):
        self.mensagem = 'A impressora matricial nao esta habilitada. Verifique as configuracoes e tente novamente.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem

class ErroImpressoraException(Exception):
    def __init__(self):
        self.mensagem = 'Nao foi possivel abrir a porta configurada. Verifique as configuracoes e tente novamente.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem

class MatrizImpressaoException(Exception):
    def __init__(self, tipo, conta, cheque):
        self.mensagem = 'Nao foi possivel imprimir '+ str(tipo) +' do cheque ' + str(cheque) + '. O modelo de cheque da conta corrente ' + str(conta) + ' nao possui esse modelo de impresssao.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem