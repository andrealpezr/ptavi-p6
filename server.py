#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

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

    def handle(self):
        method = ['INVITE', 'ACK', 'BYE']
        while 1:  # Lee línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            method = line.decode('utf-8').split(' ')
            if not line:  # Si no hay lineas en blanco sale del bucle
                break

            if method == 'INVITE':
                 mensaje = 'SIP/2.0 100 Trying\r\n\r\n'
                 mensaje += 'SIP/2.0 180 Ringing\r\n\r\n'
                 mensaje += 'SIP/2.0 200 OK\r\n\r\n'
                 self.wfile.write(mensaje)
                 print('Enviando' + mensaje)
            elif method == 'ACK':
                aEjecutar = '-/mp32rtp -i' + IP + ' -p 23032 < ' + Audio_file
                os.system('chmod 755 mp32rtp')
                print('Vamos a ejecutar', aEjecutar)
                os.system(aEjecutar)
            elif method == 'BYE':
                 self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
            elif method != 'INVITE' or 'ACK' or 'BYE':
                self.wfile.write('SIP/2.0 405 Method Not Allowed' + '\r\n\r\n')
                break
            else:
               self.wfile.write('SIP/2.0 400 Bad Request' + '\r\n\r\n')
               break

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit('Usage: python3 server.py IP port audio_file')
    else:
  # Creamos servidor de eco y escuchamos
      try:
        serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])), EchoHandler)       
        print("Listening...")
        serv.serve_forever()
      except KeyboardInterrupt:
         print(' ', 'Finalizado servidor')