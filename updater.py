import requests
import json
import os
import jsonpickle

localVersionFile = os.path.join(os.path.dirname(__file__), 'docs\\version.json')

class Updater:

    def __init__(self):
        self.url = 'https://raw.githubusercontent.com/killbills/AppCheque/master/'
        self.versionFile = 'docs/version.json'
        self.updatedFiles = 'docs/files.json'

    def checkVersion(self):
        urlVersion = self.url + self.versionFile
        response = requests.get(urlVersion).json()

        with open(localVersionFile, 'r') as file:
            localVerion = jsonpickle.decode(file.read())

        return response == localVerion

    def updade(self):
        if self.checkVersion():
            response = requests.get(self.url+'main.py')
            print(response.content)


print(Updater().updade())