#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys


if len(sys.argv) != 3:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

try:
    Method = sys.argv[1]  # MétodoSIP
    Receiver = sys.argv[2]  # Datos del receptor: login, IP, puerto
    Login = Receiver.split('@')[0] + '@'  # receptor@
    IPServer = Receiver.split('@')[1].split(':')[0]  # IP receptor
    Port = int(Receiver.split(':')[1])  # puerto IP

except (IndexError, ValueError):
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

# Contenido que vamos a enviar
Request = Method + ' ' + 'sip:' + Login + IPServer + ':' + str(Port)  + 'SIP/2.0\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IPServer, int(Port)))
