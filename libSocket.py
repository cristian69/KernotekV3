#-*- coding: utf-8 -*-
import class_db
import time
import sys
import logger
import registroVenta
import threading
import select
import os
import InhibirMDB
from libErrores import registroError  
import socket
import libVenta

IP_UDP = "127.0.0.1"
PUERTO_UDP = 8000
MESSAGE = "...."
POOL_TIME = 0.1

tarifaActual = 0  # Tarifa actual
tiempoActual = 0  # Tiempo de apertura actual
turnoActual = 0


maxIntentos = 10
DEBUG = 1

__ACTIVO__ = '1'
__INACTIVO__ = '0'

# ------ PETICIONES DEL SOCKET DE C ------	
__POOL__    = "P|x"
__TURNO__   = "T|x"
__ERROR__   = "E|"
__MONTO__   = "M|"
__TARIFA__  = "R|x"
__TIEMPO__  = "O|x"
__TICKET__  = "K|x"
__CANALES__ = "C|x"

__VENTA__ = " \x02"


#BasicValidator = "/home/linaro/projects/ITLSSPLinux_6mod/BasicValidator6/BasicValidator"
BasicValidator = "/home/odroid/projects/ITLSSPLinux_6mod/BasicValidator6/BasicValidator"

def socketC():
	try:
		os.system(BasicValidator)
	except:
		if DEBUG:
			print "No se puede iniciar el socket de C, BasicValidator encontrado revise la ruta del archivo"
		logger.error("No se puede iniciar el socket de C, BasicValidator encontrado revise la ruta del archivo")


def iniciarSocketC():
	hilo_C = threading.Thread(target=socketC, name="Hilo del socket de C")
	hilo_C.start()
# -------------------  FUNCIONES ---------------------------
def venta(msg):
    registroVenta.main(msg)


def turnoActivo():
    turno = class_db.turnoActual()
    global turnoActual
    turnoActual = turno
    turno = "T|" + str(turno)
    if DEBUG:
        print "TX: ", turno
    return turno


def tarifa():
    tarif = class_db.tarifa()
    tarif = tarif * 100
    tarif = int(tarif)
    global tarifaActual
    tarifaActual = tarif  # Guarda en la variable global la tarifa
    tarif = "R|" + str(tarif)
    if DEBUG:
        print "TX: ", tarif
    return tarif


def tiempoApertura():
    tApertura = str(class_db.tiempo_apertura())
    global tiempoActual
    tiempoActual = tApertura  # Guarda en la variable global el tiempo de apertura
    tApertura = "O|" + tApertura
    if DEBUG:
        print "TX: " + tApertura
    return tApertura



def ticket():
    ultimoTicket = int(class_db.ticket()) + 1
    ultimoTicket = "K|" + str(ultimoTicket)
    return ultimoTicket


def cambiarTarifa():
    nuevaTarifa = class_db.tarifa()  # Consulta la tarifa de la configuracion
    nuevaTarifa = int(nuevaTarifa * 100)
    if nuevaTarifa != tarifaActual:  # Si hay cambio de tarifa retorna True para mandar la nueva tarifa
        return True
    else:
        return False


def cambiarTiempoA():
    nuevoTiempo = class_db.tiempo_apertura()
    if str(nuevoTiempo) != str(tiempoActual):
        return True
    else:
        return False

#  ------------------------------  CUERPO DEL PROGRAMA -------------------------------------
def Socket():
	direccion = ""
	cambioTarifa = False
	cambioTiempo = False
	peticionesFallidas = 0
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

	while True:
		time.sleep(POOL_TIME)
		corteAutomatico = class_db.tipoCorte()
		if corteAutomatico:
			libVenta.hacerCorteAutomatico()
		
		msgSocket = select.select([sock], [], [], 0.5)

		#  ------   Banderas para monitorear los cambios al Monedero   -----
		
		cambioTarifa = cambiarTarifa()
		cambioTiempo = cambiarTiempoA()
		corteTurno = libVenta.hacerCorteTurno()
		cambioMonedero = libVenta.cambiarCanalesHoppper()
		
		if msgSocket[0]:

			class_db.estadoSocketPython(__ACTIVO__)

			peticionesFallidas = 0
			intentosActivar = 0

			RX = ""
			RX, direccion = sock.recvfrom(1024)
			if DEBUG:
			    if RX != 'P|x':
			        print "RX: %s" % (RX)

			if cambioMonedero:
				sock.sendto( libVenta.estadoCanales(), direccion )
				class_db.desactivarCambioMonedero()
				if DEBUG:
					print "Cambiando los estados de los canales del monedero"
				

			if cambioTarifa:
				sock.sendto(tarifa(), direccion)
				if DEBUG:
					print "Cambiando la tarifa a $%f" % ( tarifaActual/100 )
				logger.debug("Cambio de tarifa a $%i0" % ( tarifaActual/100 ) )

			if cambioTiempo:
				sock.sendto(tiempoApertura(), direccion)
				if DEBUG:
					print "Cambio de tiempo de apertura a %s seg." % ( tiempoActual )
				logger.debug("Cambio de tiempo de apertura a %s seg." % ( tiempoActual ) )

			if corteTurno:
				sock.sendto("M|x", direccion)
				class_db.desactivarCorteTurno()

			# ----   Selección de la operación a realizar   ----
			
			if len(RX) > 2:
				
				if RX == __TARIFA__:
					sock.sendto(tarifa(), direccion)
				
				if RX == __TIEMPO__:
					sock.sendto(tiempoApertura(), direccion)
				
				if RX == __TICKET__:
					sock.sendto(ticket(), direccion)
				
				if RX == __TURNO__:
					sock.sendto(turnoActivo(), direccion)

				if RX == __CANALES__:
					sock.sendto(estadoCanales(), direccion)
					
				if RX == __POOL__:
					sock.sendto(MESSAGE, direccion)

				if RX.startswith(__ERROR__):
					registroError(RX)

				if RX.startswith(__MONTO__):
					fondo = libVenta.totalMonto(RX)
					class_db.corteTurno(fondo)
					sock.sendto(turnoActivo(), direccion)
					if DEBUG:
						print "*" * 10, "Se realizo un corte de Turno" , "*" * 10

				if len(RX) > 70:
					if DEBUG:
						print "Venta entrante : %s" % ( RX )
					try:	
						hilo_venta = threading.Thread(target = venta, args = (RX, ), name = "Hilo para registro de la venta")
						hilo_venta.start()
					except:
						logger.error("No se puede registrar la venta, revisar la base de datos y consultas posible error con los"\
							" nombre de las columnas")
						if DEBUG:
							print "No se puede registrar la venta, revisar la base de datos y consultas posible error con los"\
							" nombre de las columnas"

		# El socket de C no constesta
		else:
			class_db.estadoSocketC(__INACTIVO__)
			peticionesFallidas += 1
			
			if DEBUG:
				print "*" * 10, " Conexion perdida ", "*" * 10

			if peticionesFallidas == maxIntentos:
				while intentosActivar < maxIntentos:
					time.sleep(0.5)
					logger.warning("Reinicio automatico del Socket C")
					if DEBUG:
						print "*" * 10, " Reinicio automatico del Socket C ", "*" * 10 
					try:
						InhibirMDB.main()
						iniciarSocketC()
						break
					except:
						intentosActivar += 1
					
				



