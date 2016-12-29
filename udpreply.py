#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Code adapted from https://pymotw.com/2/socket/udp.html

import socket
import sys

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('0.0.0.0', 9978)
print ('starting up on %s port %s' % server_address )
sock.bind(server_address)

# main loop
while True:
    print ('waiting to receive message')
    data, address = sock.recvfrom(4096)
    print ('received %s bytes from %s' % (len(data), address))
    print (data)
    # reply back if there is some data
    if data:
        sent = sock.sendto(data, address)
        print ('sent %s bytes back to %s' % (sent, address))
