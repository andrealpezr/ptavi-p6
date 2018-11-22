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
    Port = int(Receiver.split('@')[1].split(':')[1])  # puerto IP

except (IndexError, ValueError):
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IPServer, int(Port)))

# Contenido que vamos a enviar (Petición SIP)
Request = Method + ' ' + 'sip:' + Login + IPServer + ' SIP/2.0\r\n\r\n'

print('Enviando: ', Request)
my_socket.send(bytes(Request, 'utf-8') + b'\r\n\r\n')  # Para pasarlo a bytes
data = my_socket.recv(1024)

answer = data.decode('utf-8').split('\r\n\r\n')[0:-1]

if answer == ['SIP/2.0 100 Trying\r\n\r\n', 'SIP/2.0 180 Ringing\r\n\r\n',
              'SIP/2.0 200 OK\r\n\r\n']:
    ACK_Request = str('ACK' + Request)
    print("Enviando ACK:", ACK_Request)
    my_socket.send(bytes(ACK_Request, 'utf-8') + b'\r\n\r\n')
    data = my_socket.recv(1024)
elif (Method == 'BYE'):
    print('Terminando socket... BYE')
    my_socket.close()  # cerramos conexión
