#-*- coding:utf-8 -*-
__author__ = 'aramirez'
import socket
import os, os.path
import class_venta
import threading

obj_venta = class_venta
def registro_venta(datagrama):
    obj_venta.main(datagrama)

print "Conectando..."
if os.path.exists("/tmp/serversocket"):
    cliente = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    cliente.connect("/tmp/serversocket")
    print "Conectado !!"

    while True:
        datagrama = cliente.recv(1024)
        hilo_venta = threading.Thread(target=registro_venta(datagrama))
        hilo_venta.start()

        if not datagrama:
            break
        else:
            print "=" * 40
            print datagrama

print "=" * 40
print "NO se pudo Conectar"
cliente.close()
