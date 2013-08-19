# -*- coding: utf-8 -*-

from gamespy import protocol
from twisted.internet import reactor

__all__ = ['GenericGamespyClient']

class GenericGamespyClient(object):

    def __init__(self, host, port):
        self.__host__ = host
        self.__port__ = port
        self.__proto__ = protocol.Gamespy(self.__host__,
                                                  self.__port__)
        self.__listener__ = reactor.listenUDP(0, self.__proto__)


    def query_server(self):
        reactor.callLater(2, reactor.stop)
        reactor.run()

    def responses(self):
        return self.__proto__.responses
