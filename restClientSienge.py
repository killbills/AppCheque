import requests
from requests.exceptions import ConnectionError

from siengeConnectionError import TokenInvalidoException, ErroProcessamentoException, BadUrlException, TimeoutException
from configuracao import Configuracao


def get(parametros=None):
    
    _configuracao = Configuracao()
    _configuracao.carregar()

    url = _configuracao.urlSienge

    if parametros:            
        url = url + parametros

    try:
        response = requests.get(url, headers = makeHeader(_configuracao))
        if response.status_code == 401:
            raise TokenInvalidoException

        if response.status_code == 500:
            raise ErroProcessamentoException

        if response.status_code == 503:
            raise TimeoutException

        return response.json()
    except ConnectionError:
        raise BadUrlException

    
 
def makeHeader(_configuracao): 
    return {'Content-Type': 'application/json;charset=UTF-8', 'Token': _configuracao.token}