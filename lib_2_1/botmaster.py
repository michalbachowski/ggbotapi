# -*- coding: utf-8 -*-
import urllib
import urllib2
import base64
import common

from ggbotapi.lib_2_1.authentication import Authentication


class Error(common.Error):
    pass


class AdapterNotSetError(Error):
    pass


class AuthenticationNotSetError(Error):
    pass


class BotAuthenticationError(Error):
    pass


class TooLongStatusError(Error):
    pass


class UnknownStatusError(Error):
    pass


class Status(object):
    FFC = 2
    BUSY = 3
    FFC_WITH_DESC = 4
    BUSY_WITH_DESC = 5

    INVISIBLE = 20
    OFFLINE_WITH_DESC = 21
    INVISIBLE_WITH_DESC = 22

    TALK_TO_ME = 23
    TALK_TO_ME_WITH_DESC = 24
    DND = 33
    DND_WITH_DESC = 34

    def __init__(self, status):
        if status not in [self.FFC, self.BUSY, self.FFC_WITH_DESC, \
            self.BUSY_WITH_DESC, self.INVISIBLE, self.OFFLINE_WITH_DESC, \
            self.INVISIBLE_WITH_DESC, self.TALK_TO_ME, \
            self.TALK_TO_ME_WITH_DESC, self.DND, self.DND_WITH_DESC]:
            raise UnknownStatusError('Given status is unknown.')
        self._status = status

    def __int__(self):
        return self._status


class Client(object):

    tokenDiscoveryUrl = 'https://botapi.gadu-gadu.pl/botmaster/getToken/%u'
    #tokenDiscoveryUrl = 'http://localhost:8866/%u'
    pushUrl = 'http://%s:%u/%s/%u'

    def __init__(self, adapter=None, authentication=None):
        """
        Prepares object instance

        CommunicationAdapter    adapter
        Authentication          authentication
        """
        self._adapter = adapter
        if authentication is not None:
            authentication.botmaster = self
        self._auth = authentication

    def adapter(self, adapter=None):
        """
        Fetches current communication adapter.
        If adapter is given - replaces current instance.

        CommunicationAdapter     adapter
        return  CommunicationAdapter
        """
        if adapter is not None:
            self._adapter = adapter
        if self._adapter is None:
            self._adapter = UrllibAdapter()
        if self._adapter is None:
            raise AdapterNotSetError('Communication Adapter not set')
        return self._adapter

    def auth(self, botID=None, login=None, password=None):
        """
        Fetches current authentication adapter.
        If credentials are given - adapter is instantinated.

        int     botID
        str     login
        str     password
        return  Authentication
        """
        if botID is not None:
            self._auth = Authentication(botID, login, password, self)
        if self._auth is None:
            raise AuthenticationNotSetError('Authentication not set')
        if not self._auth.is_valid():
            raise BotAuthenticationError('Could not authenticate')
        return self._auth

    def authorize(self, botID, login, password):
        """
        Issues autorization request

        int     botID
        str     login
        str     password
        return  str
        """
        # prepare basic authorization header
        auth = base64.b64encode('%s:%s' % (login, password))
        return self.call(self.tokenDiscoveryUrl % botID,\
            {'Authorization': 'Basic %s' % auth})

    def get_push_url(self, action):
        credentials = self.auth().credentials
        return self.pushUrl % (credentials.server, credentials.port, \
            action, credentials.botID)

    def send(self, message, recipients, sendToOffline=True):
        """
        Sends message

        str     message
        list    recipients
        bool    sendToOffline
        return  str
        """
        credentials = self.auth().credentials
        url = self.get_push_url('sendMessage')
        data = {\
            'to': ','.join(map(str, recipients)),\
            'token': credentials.token,\
            'msg': message}
        headers = {\
            'Content-Type': 'application/x-www-form-urlencoded'}
        headers['Send-to-offline'] = int(sendToOffline)
        return self.call(url, headers, data)

    def set_status(self, status, desc):
        """
        Sets bot status

        int     status  status number
        str     desc    status description
        return  str
        """
        credentials = self.auth().credentials
        url = self.get_push_url('setStatus')
        if len(desc) > 255:
            raise TooLongStatusError('Status description could not be ' \
                + 'longer than 255 chars')
        data = {\
            'token': credentials.token,\
            'status': int(status),\
            'desc': desc}
        return self.call(url, {}, data)

    def call(self, url, headers, data=None):
        """
        Sends request to botmaster

        str     url
        dict    headers
        dict    data        data to send (using POST request)
        return  str
        """
        return self.adapter().call(url, headers, data)


class CommunicationAdapter(object):

    def __init__(self, debug=0):
        """
        Prepares object instance

        int     debug
        """
        pass

    def call(self, url, headers, data=None):
        """
        Issues request to botmaster

        str     url
        dict    headers
        dict    data        data to send (using POST request)
        return  str
        """
        pass


class UrllibAdapter(CommunicationAdapter):

    def __init__(self, debug=0):
        """
        Prepares object instance

        int     debug
        """
        self.opener = urllib2.build_opener(\
            urllib2.HTTPHandler(debuglevel=debug))

    def call(self, url, headers, data=None):
        """
        Issues HTTP request

        str     url
        dict    headers
        dict    data        data to send (using POST request)
        return  str
        """
        if type(dict()) == type(data):
            data = urllib.urlencode(data)
        request = urllib2.Request(url, data)
        # append headers
        for (header, value) in headers.iteritems():
            request.add_header(header, value)
        # make request
        try:
            return self.opener.open(request).read()
        except Exception, e:
            raise Error(e)
