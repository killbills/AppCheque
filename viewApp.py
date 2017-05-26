import os
import sys
import platform
import json
import logging
import time

from cefpython3 import cefpython as cef
from configuracao import Configuracao
from mensagemApp import sucesso
from mensagemApp import falha

WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")
WINDOWS_UTILS = cef.WindowUtils()


class Gui(object):
    def window(self):
        path= os.path.join(os.path.dirname(__file__), 'view\\viewApp.html')
        browser = cef.CreateBrowserSync(url=path, window_title="Cheques",)
        set_javascript_bindings(browser)
        cef.MessageLoop()


def set_javascript_bindings(browser):
    bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
    bindings.SetFunction("buscarConfiguracao", buscarConfiguracao)
    bindings.SetFunction("salvarConfiguracao", salvarConfiguracao)
    bindings.SetFunction("sairApp", sairApp)
    browser.SetJavascriptBindings(bindings)


def sairApp(callback=None):
    logging.info("Shutdown - " + time.strftime('%c'))
    sys.exit()


def salvarConfiguracao(jsonConfiguracao, callback=None):
    try:

        configuracao = Configuracao()
        configuracao.parseFromJson(json.dumps(jsonConfiguracao, sort_keys=True, indent=4))
        print(json.dumps(jsonConfiguracao, sort_keys=True, indent=4))
        configuracao.salvar()

        if callback:
            callback.Call(sucesso("Configuracao atualizada."))
        else:
            return falha("Houve uma falha ao salvar a configuracao.")

    except Exception as e:
        callback.Call(falha("Ocorreu uma falha ao salvar a configuracao."))


def buscarConfiguracao(callback=None):
    configuracao = Configuracao()
    configuracao.carregar()
    if callback:
        callback.Call(configuracao.__dict__)
    else:
        return configuracao.__dict__


def carregarTela():
    check_versions()

    sys.excepthook = cef.ExceptHook

    settings = {
        "debug": True,
        "log_severity": cef.LOGSEVERITY_ERROR,
        "log_file": "debug.log",
        "product_version": "PyCheque/1.00",
        "user_agent": "PyCheque/1.00",
    }

    if WINDOWS:
        settings["auto_zooming"] = "system_dpi"
        cef.DpiAware.SetProcessDpiAware()

    cef.Initialize(settings=settings)

    app = Gui()
    app.window()

    print("Close")
    sys.exit()


def check_versions():
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
