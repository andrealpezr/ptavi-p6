#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


if len(sys.argv) != 3:
    sys.exit('Usage: python3 client.py method receiver@IP=SIPport')

METODO = sys.argv[1]
RECEPTOR = sys.argv[2]
IP =
PORT =

# Contenido que vamos a enviar
LINE = METODO + ' ' + 'sip:' + IP + ' ' + 'SIP/2.0'


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, PORT))

    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    print('Recibido -- ', data.decode('utf-8'))
    print("Terminando socket...")

print("Fin.")
