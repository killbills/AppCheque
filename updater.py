import requests
import json
import os
import jsonpickle
import urllib2
from datetime import datetime
import time

localPath = os.path.dirname(__file__)
localVersionFile = os.path.join(localPath, 'docs\\version.json')

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

    def update(self):
        if not self.checkVersion():
            urlFiles = self.url + self.updatedFiles
            files = json.loads(json.dumps(requests.get(urlFiles).json()))
            for f in files['files']:
                updatedFile = urllib2.urlopen(self.url+str(f['file']))
                with open (os.path.join(localPath, str(f['file'])), 'w') as output:
                    output.write(updatedFile.read())
            



def updateVersion():
    with open(os.path.join(localPath, 'docs\\lastUpdate.json'), 'r') as file:
        lastUpdate = jsonpickle.decode(file.read())

        Updater().update()