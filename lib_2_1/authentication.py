# -*- coding: utf-8 -*-
from lxml import etree

from botmaster import Client


class Credentials(object):
    botID = None
    token = None
    server = None
    port = None

    def __init__(self, botID):
        self.botID = botID

    def fromXml(self, xml):
        root = etree.XML(xml)
        self.token = root.find('token').text
        self.server = root.find('server').text
        self.port = int(root.find('port').text)


class Authentication(object):

    def __init__(self, botID, login, password, botmaster=None):
        self.credentials = Credentials(botID)
        self.login = login
        self.password = password
        self.botmaster = botmaster
        self.valid = None
        
    def is_valid(self):
        if self.valid is None:
            self.reload()
        return self.valid

    def reload(self):
        self.credentials.fromXml(\
            self.load_credentials())
        self.valid = self.credentials.token is not None

    def load_credentials(self):
        return self.botmaster.authorize(self.credentials.botID,\
            self.login, self.password)

