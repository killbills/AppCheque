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

class MatrizImpressaoVersoException(Exception):
    def __init__(self, conta, cheque):
        self.mensagem = 'Nao foi possivel imprimir o verso do cheque ' + str(cheque) + '. O modelo de cheque da conta corrente ' + str(conta) + ' nao possui esse modelo de impresssao.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem

class MatrizImpressaoCopiaException(Exception):
    def __init__(self, conta, cheque):
        self.mensagem = 'Nao foi possivel imprimir a copia do cheque ' + str(cheque) + '. O modelo de cheque da conta corrente ' + str(conta) + ' nao possui esse modelo de impresssao, ou o Parametro 295 esta configurado como \'Nao\'. Verifique as configuracoes da conta corrente e do parametro 295.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem