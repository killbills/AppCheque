import json
import traceback
import logging
import time
import os

from restClientSienge import get as consumirSiengeAPI
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from armanezamentoCheque import ArmanezamentoCheque
from controleImpressao import ControleImpressao
from siengeConnectionError import TokenInvalidoException, ErroProcessamentoException, BadUrlException, TimeoutException
from printerException import ImpressoraSerialNaoConfiguradaException, ImpressoraMatricialNaoConfiguradaException, ErroImpressoraException, MatrizImpressaoException
from mensagemApp import sucesso, falha

HOST_NAME = 'localhost'
PORT_NUMBER = 9151
HTTP_CODE_OK = 200
HTTP_CODE_INTERNAL_SERVER_ERROR = 500

server = None


class Handler(BaseHTTPRequestHandler):
    def _set_headers_sucess(self):
        self.send_response(HTTP_CODE_OK)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def _set_headers_fail(self):
        self.send_response(HTTP_CODE_INTERNAL_SERVER_ERROR)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_GET(self):
        try:
            dataInicio = self.path[1:]

            cheques = consumirSiengeAPI(dataInicio)

            armazenamentoJsonCheques = ArmanezamentoCheque(cheques)
            armazenamentoJsonCheques.salvar();

            self._set_headers_sucess()
            self.wfile.write(json.dumps(cheques).encode())

        except TokenInvalidoException as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha(e.getMessage())).encode())
            logging.warn(e.getMessage())

        except ErroProcessamentoException as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha(e.getMessage())).encode())
            logging.warn(e.getMessage())

        except BadUrlException as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha(e.getMessage())).encode())
            logging.warn(e.getMessage())

        except TimeoutException as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha(e.getMessage())).encode())
            logging.warn(e.getMessage())

        except Exception as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha("Ocorreu um erro inesperado na conexao com o Sienge. Entre em contato com o suporte Sienge")).encode())
            logging.error(traceback.format_exc())

    def do_POST(self):
        try:
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            jsonImpressao = json.loads(self.data_string)
            ControleImpressao(jsonImpressao['ids']).imprimirCheques(jsonImpressao['copia'], jsonImpressao['verso'])

            self._set_headers_sucess()
            self.wfile.write(json.dumps(sucesso("Cheque(s) impresso(s) com sucesso.")).encode())

        except ImpressoraMatricialNaoConfiguradaException as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha(e.getMessage())).encode())
            logging.warn(e.getMessage())            

        except ImpressoraSerialNaoConfiguradaException as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha(e.getMessage())).encode())
            logging.warn(e.getMessage())

        except ErroImpressoraException as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha(e.getMessage())).encode())
            logging.warn(e.getMessage())

        except MatrizImpressaoException as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha(e.getMessage())).encode())
            logging.warn(e.getMessage())

        except Exception as e:
            self._set_headers_fail()
            self.wfile.write(json.dumps(falha("Ocorreu um erro inesperado na impressao. Entre em contato com o suporte Sienge")).encode())
            logging.error(traceback.format_exc())


def iniciarServidor():
    path=os.path.join(os.path.dirname(__file__), 'logs\\appCheque.log')
    logging.basicConfig(filename=path, level=logging.INFO)
    logging.info('Started - ' + time.strftime('%c'))
    server = HTTPServer((HOST_NAME, PORT_NUMBER), Handler)
    server.serve_forever()
