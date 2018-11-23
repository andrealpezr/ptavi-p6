#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor @author: Andrea."""

import socket
import sys


SIP = ""

if len(sys.argv) != 3:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

try:
    Method = sys.argv[1]  # Método SIP
    Receiver = sys.argv[2]  # Datos del receptor
    Port = int(Receiver.split(":", -1)[1])  # Puerto IP
    SIP = "sip:" + Receiver.split(":", -1)[0] + " SIP/2.0\r\n\r\n"  # Mensaje
except(IndexError, ValueError):
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")


if Method == "INVITE":
    ANSWER = "INVITE " + SIP
elif Method == "BYE":
    ANSWER = "BYE " + SIP

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect(('127.0.0.1', Port))

my_socket.send(bytes(ANSWER, 'utf-8') + b'\r\n\r\n')  # Para pasarlo a bytes
data = my_socket.recv(1024)
print(data.decode('utf-8'))
data = data.decode('utf-8').split()

if data[1] == '100' and data[4] == '180' and data[7] == '200':
    ANSWER = "ACK " + SIP
    print('Sending ACK...')
    my_socket.send(bytes(ANSWER, 'utf-8') + b'\r\n\r\n')  # Pasamos a bytes

print('Ending socket... BYE')
my_socket.close()  # Cerramos conexión
