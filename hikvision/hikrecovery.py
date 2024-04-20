#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Some code from https://github.com/sirMackk/py3tftp/blob/master/py3tftp/protocols.py
# and other from https://docs.python.org/3/library/asyncio-protocol.html#udp-echo-server

from asyncio import get_event_loop
from logging import getLogger, DEBUG, basicConfig as logging_basicConfig
from py3tftp.protocols import BaseTFTPServerProtocol, RRQProtocol
from py3tftp.file_io import FileReader
from py3tftp.exceptions import ProtocolException


logging_basicConfig(level=DEBUG)
logger = getLogger(__name__)
logger.setLevel(DEBUG)


class MyTFTPServerProtocol(BaseTFTPServerProtocol):
    def select_protocol(self, packet):
        logger.debug('packet type: {}'.format(packet.pkt_type))
        if packet.is_rrq():
            return RRQProtocol
        elif packet.is_wrq():
            raise ProtocolException("I'm not here to receive files!")
            # return WRQProtocol
        else:
            raise ProtocolException('Received incompatible request, ignoring.')

    def select_file_handler(self, packet):
        if packet.is_rrq():
            return lambda filename, opts: FileReader(
                'digicap.dav', opts, packet.mode)


class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        logger.info('Received %r from %s', message, addr)
        logger.info('Send %r to %s', message, addr)
        self.transport.sendto(data, addr)


def main():
    logger.info('Starting TFTP server')

    loop = get_event_loop()

    listen_tftp = loop.create_datagram_endpoint(
        lambda: MyTFTPServerProtocol('192.0.0.128', loop, {}),
        local_addr=('192.0.0.128', 69,))

    listen_echo = loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('192.0.0.128', 9978,))

    transport_tftp, protocol_tftp = loop.run_until_complete(listen_tftp)
    transport_echo, protocol_echo = loop.run_until_complete(listen_echo)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Received signal, shutting down')

    transport_tftp.close()
    transport_echo.close()
    loop.close()


if __name__ == '__main__':
    main()


# # Create a UDP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # Bind the socket to the port
# server_address = ('0.0.0.0', 9978)
# print ('starting up on %s port %s' % server_address )
# sock.bind(server_address)

# # main loop
# while True:
#     print ('waiting to receive message')
#     data, address = sock.recvfrom(4096)
#     print ('received %s bytes from %s' % (len(data), address))
#     print (data)
#     # reply back if there is some data
#     if data:
#         sent = sock.sendto(data, address)
#         print ('sent %s bytes back to %s' % (sent, address))
