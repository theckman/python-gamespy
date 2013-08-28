#!/usr/bin/env python

# -*- coding: utf-8 -*-

import json
import gamespy.clients

if __name__ == "__main__":
    server_ip = "70.42.74.59"
    server_port = 2302

    # create new ArmA 2 client, provide IP and port
    c = gamespy.clients.ArmA2OA(server_ip, server_port)

    # ask the server for information
    c.query_server()

    # parse the response and build a dict
    c.parse_response()

    # get the data
    data = c.data()

    # print the data, use json.dumps() to make it pretty
    print(json.dumps(data, indent=4))
