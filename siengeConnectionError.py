class TokenInvalidoException(Exception):

    def __init__(self):
        self.mensagem = 'Token invalido. Verifique as configuraoces de acesso no Sienge e tente novamente.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem


class ErroProcessamentoException(Exception):
    def __init__(self):
        self.mensagem = 'Ocorreram erros durante o processamento. Entre em contato com o Suporte Sienge.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem


class TimeoutException(Exception):
    def __init__(self):
        self.mensagem = 'O servidor esta demorando muito para responder. Verifique os filtros utilizados e tente novamente.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem


class BadUrlException(Exception):
    def __init__(self):
        self.mensagem = 'A URL de acesso ao Sienge pode estar incorreda. Verifique as configuracoes de acesso ao Sienge e tente novamente.'
    
    def __str__(self):
        return repr(self.mensagem)

    def getMessage(self):
        return self.mensagem