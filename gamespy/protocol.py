# -*- coding: utf-8 -*-

import struct
import time
import gamespy.exceptions as E
from twisted.internet.protocol import ConnectedDatagramProtocol

__all__ = ['Gamespy']


class Gamespy(ConnectedDatagramProtocol):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.responses = ()
        self.__token__ = None

    def startProtocol(self):
        self.transport.connect(self.host, self.port)
        self.send_hello()

    def datagramReceived(self, datagram, addr):
        reply = int(struct.unpack("!B", datagram[0])[0])

        if reply == 9:
            self.__token__ = datagram[5:].strip('\x00')
            self.send_request()
        elif reply == 0:
            scratch = []
            for response in self.responses:
                scratch.append(response)
            scratch.append(datagram)
            self.responses = tuple(scratch)
            del scratch
        else:
            raise E.UnknownResponseType("{0} is an unknown "
                                        "response type".format(reply))

    def send_hello(self):
        self.transport.write(struct.pack("!3Bi", 0xFE, 0xFD, 0x09,
                                         int(time.time())))

    def send_request(self):
        self.transport.write(struct.pack("!3Bii4B", 0xFE, 0xFD, 0x00,
                                         int(time.time()), int(self.__token__),
                                         0xFF, 0xFF, 0xFF, 0x01))

    def reset(self):
        self.responses = ()
        self.__token__ = None
