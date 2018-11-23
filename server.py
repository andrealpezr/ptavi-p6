#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import os


try:
        IP = sys.argv[1]
        Port = int(sys.argv[2])
        Audio_file = sys.argv[3]

except (IndexError, ValueError):
    sys.exit('Usage: python3 server.py IP port audio_file')


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    def handle(self):
        """ENVIA MENSAJE AL CLIENTE."""
        # Lee línea a línea lo que nos envía el cliente
        line = self.rfile.read()
        print("El cliente nos envía " + line.decode('utf-8'))
        methods = line.decode('utf-8').split()
        method = methods[0]

        if method == 'INVITE':
            if method[1].split('@'):
                mensaje = b'SIP/2.0 100 Trying\r\n\r\n'
                mensaje += b'SIP/2.0 180 Ringing\r\n\r\n'
                mensaje += b'SIP/2.0 200 OK\r\n\r\n'
                self.wfile.write(mensaje)
            else:
                self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')
        elif method == 'ACK':
            aEjecutar = 'mp32rtp -i' + ' ' + IP + ' -p 23032 < ' + Audio_file
            print('Vamos a ejecutar', aEjecutar)
            os.system(aEjecutar)
            print('Audio enviado')
        elif method == 'BYE':
            self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
        elif method != 'INVITE' or 'ACK' or 'BYE':
            self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')
        else:
            self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit('Usage: python3 server.py IP port audio_file')
    else:  # Creamos servidor de eco y escuchamos
        try:
            serv = socketserver.UDPServer((IP, Port), EchoHandler)
            print("Listening...")
            serv.serve_forever()
        except KeyboardInterrupt:
            print(' ', 'Finalizado servidor')
