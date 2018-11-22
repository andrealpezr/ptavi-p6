#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor."""

import socket
import sys


SIP = ''

if len(sys.argv) != 3:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

try:
    Method = sys.argv[1]  # MétodoSIP
    Receiver = sys.argv[2]  # Datos del receptor: login, IP, puerto
    IPServer = Receiver.split('@')[1].split(':')[0]  # IP receptor
    Port = int(Receiver.split('@')[1].split(':')[1])  # puerto IP

except (IndexError, ValueError):
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

# Contenido que vamos a enviar (Petición SIP)
Request = 'sip:' + IPServer + ' SIP/2.0\r\n\r\n'

if Method == 'INVITE':
    ANSWER = 'INVITE' + SIP
elif Method == 'BYE':
    ANSWER = 'BYE' + SIP

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect(('127.0.0.1', Port))

print('Sending: ' + Request)
my_socket.send(bytes(ANSWER, 'utf-8') + b'\r\n\r\n')  # Para pasarlo a bytes
data = my_socket.recv(1024)
print('Answer server...', data.decode('utf-8'))
data = data.decode('utf-8').split()

if data == ('SIP/2.0 100 Trying\r\n\r\n', 'SIP/2.0 180 Ringing\r\n\r\n',
              'SIP/2.0 200 OK\r\n\r\n'):
    ANSWER = 'ACK' + SIP
    print('Sending ACK...')
    my_socket.send(bytes(ANSWER, 'utf-8') + b'\r\n\r\n')

print('Ending socket... BYE')
my_socket.close()  # cerramos conexión