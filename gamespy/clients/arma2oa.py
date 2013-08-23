# -*- coding: utf-8 -*-


import struct
import itertools
import collections
import pprint
import json
from .generic import GenericGamespyClient
from twisted.internet import reactor

__all__ = ['ArmA2OA']


class ArmA2OA(GenericGamespyClient):

    def __init__(self, host, port):
        super(ArmA2OA, self).__init__(host, port)
        self.__data__ = {}

    def query_server(self):
        reactor.callLater(2, reactor.stop)
        reactor.run()

    def __clean_list__(self, packet):
        try:
            while True:
                packet.remove('')
        except:
            pass
        return packet

    def __update_data__(self, data_points):
        for point in data_points:
            if type(point[1]) in [type(int()), type(str())]:
                self.__data__[point[0]] = point[1]
            else:
                self.__data__[point[0]] = tuple(point[1:])

    def __header_packet__(self, packet):
        packet = packet[2:].split('\x00')
        # print("{0}{1}{1}".format(repr(packet), "\n"))
        for pair in itertools.izip(*[iter(packet)]*2):
            self.__data__[pair[0]] = pair[1]

    def __second_packet__(self, packet):
        packet = self.__clean_list__(packet[1:].split('\x00'))
        data_points = []
        # print("{0}{1}{1}".format(repr(packet), "\n"))
        for pair in itertools.izip(*[iter(packet)]*2):
            if pair[0] == "\x01player_":
                # players
                start = packet.index('\x01player_') + 1
                end = packet.index('team_')
                players = self.__clean_list__(packet[start:end])
                player_dict = {key: {} for key in players}

                # teams
                start = packet.index('team_') + 1
                end = packet.index('score_')
                self.__data__['teams'] = self.__clean_list__(packet[start:end])

                # score
                start = packet.index('score_') + 1
                end = packet.index('deaths_')
                scores = self.__clean_list__(packet[start:end])
                for player_index, score in enumerate(scores):
                    player_dict[players[player_index]]['score'] = score

                # deaths
                start = packet.index('deaths_') + 1
                end = packet.index('\x02')
                deaths = self.__clean_list__(packet[start:end])
                for player_index, death in enumerate(deaths):
                    player_dict[players[player_index]]['deaths'] = death

                self.__data__['player_list'] = tuple(players)
                self.__data__['players'] = player_dict
            else:
                if self.__data__.get('player_list', False):
                    break
                else:
                    self.__data__[pair[0]] = pair[1]

    def parse_response(self):
        for packet in self.responses():
            packet = packet[14:]
            #print("{0}{1}{1}".format(repr(packet), "\n"))
            splitnum = struct.unpack("!B", packet[0])[0]
            if splitnum == 0:
                self.__header_packet__(packet)
            elif "\x01player_" in packet:
                self.__second_packet__(packet[1:])

    def data(self):
        if not len(self.__data__):
            self.parse_response()
        return self.__data__
