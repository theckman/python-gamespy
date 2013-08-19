# -*- coding: utf-8 -*-


class GamespyProtocolException(Exception):
    pass


class GamespyClientException(Exception):
    pass


class UnknownResponseType(GamespyProtocolException):
    pass
