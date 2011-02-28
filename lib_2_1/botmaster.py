# -*- coding: utf-8 -*-
import urllib2
import base64
import common


class Error(common.Error):
    pass


class Client(object):

    tokenDiscoveryUrl = 'https://botapi.gadu-gadu.pl/botmaster/getToken/%u'
    #tokenDiscoveryUrl = 'http://localhost:8866/%u'
    pushUrl = '%s:%u/%u'

    def __init__(self, adapter=None):
        self.adapter = adapter

    def authorize(self, botID, login, password):
        # prepare basic authorization header
        auth = base64.b64encode('%s:%s' % (login, password))
        return self.call(self.tokenDiscoveryUrl % botID,\
            {'Authorization': 'Basic %s' % auth})

    def send(self, credentials, message, recipients, sendToOffline=True):
        # use credentials...
        url = ''
        headers = {}
        headers['To'] = ','.join(recipients)
        if not sendToOffline:
            headers['Send-to-offline'] = 0
        return self.call(url, headers, message)

    def call(self, url, headers, message=None):
        return self.adapter.call(url, headers, message)


class CommunicationAdapter(object):
    def __init__(self, debug=0):
        pass

    def call(self, url, headers, message=None):
        pass


class UrllibAdapter(CommunicationAdapter):
 
    def __init__(self, debug=0):
        self.opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=debug))

    def call(self, url, headers, message=None):
        request = urllib2.Request(url)
        # append headers
        for (header, value) in headers.iteritems():
            request.add_header( header, value )
        # make request
        try:
            return self.opener.open(request).read()
        except Exception, e:
            raise Error(e)
