#-*- coding: utf-8 -*-
import class_db
import time
import sys
import logger
import registroVenta
import threading
import select
import os


IP_UDP = "127.0.0.1"
PUERTO_UDP = 8000
MESSAGE = "...."

tarifaActual = 0  # Tarifa actual
tiempoActual = 0  # Tiempo de apertura actual
turnoActual = 0

maxIntentos = 30
DEBUG = 0

#BasicValidator = "/home/linaro/projects/ITLSSPLinux_6mod/BasicValidator6/BasicValidator"
BasicValidator = "/home/odroid/projects/ITLSSPLinux_6mod/BasicValidator6/BasicValidator"

def socketC():
	try:
		os.system(BasicValidator)
	except:
		if DEBUG:
			print "No se puede iniciar el socket de C, BasicValidator encontrado revise la ruta del archivo"
		logger.error("No se puede iniciar el socket de C, BasicValidator encontrado revise la ruta del archivo")


def main():
	cambioTarifa = False
	cambioTiempo = False
	contador = 0
	corteTurno = False
	cambioMonedero = False
	corteAutomatico = False
	if DEBUG:
		print "Conectando a %s por el puerto %i" % (IP_UDP, PUERTO_UDP)
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((IP_UDP, PUERTO_UDP))
		sock.setblocking(0)
		if DEBUG:
			print "Iniciando Conexión"
		sock.sendto("Iniciando socket", (IP_UDP, PUERTO_UDP))
		if DEBUG:
			print "Conexión establecida"
		class_db.estadoSocketPython('1')
	except:
		if DEBUG:
			print "No se puede iniciar el socket de python, la dirreción o puerto pude estar ocupada por otro proceso"
		logger.error("No se puede iniciar el socket de python, la dirreción o puerto pude estar ocupada por otro proceso")
		sys.exit(0)



