# -*- coding: utf-8 -*-
import struct
import binascii

import common


class MessageBuilderError(common.Error):
    pass


class NoTextMessageError(MessageBuilderError):
    pass


class NoHtmlMessageError(MessageBuilderError):
    pass


class MessageBuilder(object):

    def __init__(self):
        self.clear()

    def clear(self):
        """
        Resets internal state to default values

        return MessageBuilder
        """
        self.txt = ''
        self.html = ''
        self.htmlFormatted = ''
        self.formatting = ''
        self.img = None
        self.response = None
        return self

    def add_text(self, message, newLine=True):
        """
        Adds new piece of PLAIN TEXT message

        str     message
        bool    newLine     whether to prepend message with new line
        return  MessageBuilder
        """
        if newLine and len(self.txt) > 0:
            self.txt += "\r\n"
        self.txt += message
        return self

    def add_html(self, message, newLine=True):
        """
        Adds new piece of HTML message

        str     message
        bool    newLine     whether to prepend message with new line
        return  MessageBuilder
        """
        if newLine and len(self.html) > 0:
            self.html += "<br />"
        self.html += message
        return self

    def __str__(self):
        return self.build(True)

    def build(self, includeImage=False):
        """
        Returns message. Caches build message for further retrival.

        bool    includeImage    whether include image in response or not
        return  str
        """
        if self.response is None:
            self.response = self._build(includeImage)
        return self.response

    def _build(self, includeImage=False):
        """
        Builds message

        bool    includeImage    whether include image in response or not
        return  str
        """
        if self.txt is None:
            raise NoTextMessageError('Text message could not be set to None ' \
                + '(it could be however set to empty string)')
        if self.html is None:
            raise NoHtmlMessageError('HTML message could not be set to None ' \
                + '(it could be however set to empty string)')


        self.htmlFormatted = ("""<span style="color:#000000; """ \
            + """font-family:'MS Shell Dlg 2'; font-size:9pt; ">%s</span>""") \
            % self.html
        return "%s%s\0%s\0%s%s" \
            % (self.lengths(includeImage), self.htmlFormatted, \
                self.txt, self.image(), self.format())

    def lengths(self, includeImage=False):
        return struct.pack('IIII', \
            len(self.htmlFormatted) + 1, len(self.txt) + 1, \
            self.calculateImageLength(includeImage), \
            self.calculateFormatLength())

    def calculateImageLength(self, includeImage=False):
        if self.img is None:
            return 0
        if not includeImage:
            return 16
        return 16 + len(self.img)

    def calculateFormatLength(self):
        if 0 == len(self.formatting):
            return 0
        return len(self.formatting) + 3

    def image(self, includeImage=False):
        if self.img is None:
            return ''
        checksum = "%08x%08x" % (binascii.crc32(self.img) & 0xffffffff, \
            len(self.img))
        if includeImage:
            checksum += self.img
        return checksum

    def format(self):
        if self.formatting is None:
            return ''
        if 0 == len(self.formatting):
            return ''
        return struct.pack('Cv', 0x02, len(self.formatting) + self.formatting)
