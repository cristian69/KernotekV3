#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import socket
import time
import sys
import logger
import registroVenta
import threading
import select
import os
import class_db
import InhibirMDB
from libErrores import registroError
from datetime import datetime
import libgral

CONTADOR_CORTE = 0
BANDERA_CORTE = True
IP_UDP = "127.0.0.1"
PUERTO_UDP = 8000
MESSAGE = "...."

tarifaActual = 0  # Tarifa actual
tiempoActual = 0  # Tiempo de apertura actual
turnoActual = 0

maxIntentos = 20
DEBUG = 1

# BasicValidator = "/home/linaro/projects/ITLSSPLinux_6mod/BasicValidator6/BasicValidator"
BasicValidator = "/home/odroid/projects/ITLSSPLinux_6mod/BasicValidator6/BasicValidator"
def socketC():
    try:
        os.system(BasicValidator)
    except:
        if DEBUG:
            print "EL ARCHIVO BasicValidator.c no se encuentra"
        logger.error('BasicValidator.c no se encuentra')


def iniciarThread():
    if DEBUG:
        print "INCIANDO EL DRIVER DE C"
    try:
        hiloC = threading.Thread(target=socketC)
        hiloC.start()
    except:
        if DEBUG:
            print "NO SE PUEDE INICIAR EL SOCKET DE C"
        class_db.estadoSocketC('0')


def Socket():
    cambioTarifa = False
    cambioTiempo = False
    contador = 0
    corteTurno = False
    cambioMonedero = False
    corteAutomatico = False

    print "Conectando a ", IP_UDP
    print "Puerto ", PUERTO_UDP

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP_UDP, PUERTO_UDP))
    sock.setblocking(0)

    try:
        print "Estableciendo la conexión..."
        sock.sendto("Iniciando socket  UDP", (IP_UDP, PUERTO_UDP))
        print "Conexión establecida"
        class_db.estadoSocketPython('1')  # Registra que el socket de python esta corriendo
    except:
        if DEBUG:
            print "No se puede Iniciar el Soceket de Python"
        class_db.estadoSocketPython('0')  # Registra que el socket python no se pudo inciar
        logger.error("No se puede conectar Socket")
        sys.exit(0)
    while True:
        corteAutomatico = class_db.tipoCorte()
        if corteAutomatico:
            hacerCorteAutomatico()

        time.sleep(0.01)  # Tiempo de poleo
        datosSocket = select.select([sock], [], [], 0.5)
        cambioTarifa = cambiarTarifa()  # Cambio de tarifa
        cambioTiempo = cambiarTiempoA()  # Cambio de tiempo de apertura
        corteTurno = hacerCorteTurno()  # Realizar un corte de turno
        cambioMonedero = cambiarCanalesHopper()  # Cambiar los canales del mondero
        if datosSocket[0]:
	    contador = 0
            mensajeSocket = ""
            mensajeSocket, direccion = sock.recvfrom(1024)
            if DEBUG:
		if mensajeSocket != "P|x":
                    print "RX: ", mensajeSocket

            if cambioMonedero:
                if DEBUG:
                    print "Realizando cambios en los canales del monedero"
                sock.sendto(estadoCanales(), direccion)
                class_db.desactivarCambioMonedero()

            if cambioTarifa:
                sock.sendto(tarifa(), direccion)
                if DEBUG:
                    print "CAMBIO DE TARIFA A : ", tarifa()
                logger.debug("Cambio de tarifa a $%i.00" % ( tarifaActual/100 ) )

            if cambioTiempo:
                sock.sendto(tiempoApertura(), direccion)
                if DEBUG:
                    print "CAMBIO DE TIEMPO DE APERTURA A : ", tiempoApertura()
                logger.debug("Cambio de tiempo de apertura a %s seg." % ( tiempoActual ) )

            if corteTurno:
                if DEBUG:
                    print "CORTE DE TURNO REALIZADO"
                sock.sendto("M|x", direccion)
                class_db.desactivarCorteTurno()

            if len(mensajeSocket) > 2:
                if mensajeSocket.startswith("R|x"):
                    sock.sendto(tarifa(), direccion)
                elif mensajeSocket.startswith("O|x"):
                    sock.sendto(tiempoApertura(), direccion)
                elif mensajeSocket.startswith("K|x"):
                    sock.sendto(ticket(), direccion)
                elif mensajeSocket.startswith("T|x"):
                    sock.sendto(turnoActivo(), direccion)
                elif mensajeSocket.startswith("P|x"):
                    sock.sendto(MESSAGE, direccion)
                elif mensajeSocket.startswith("E|"):
                    registroError(mensajeSocket)
                if mensajeSocket.startswith("M|"):
                    fondo = totalMonto(mensajeSocket)
                    class_db.corteTurno(fondo)
                    sock.sendto(turnoActivo(), direccion)
                if mensajeSocket.startswith("C|x"):
                    sock.sendto(estadoCanales(), direccion)
                if mensajeSocket.startswith('\x02') and len(mensajeSocket) > 70:
                    if DEBUG:
                        print "VENTA ENTRANTE: ", mensajeSocket
                    #try:
                    hilo_venta = threading.Thread(target=venta(mensajeSocket))
                    hilo_venta.start()
                    #except:
                    #    print "No se puede iniciar el registro de la venta"
                        
                        #logger.error("ERROR CON LAS FOREING KEY")

            class_db.estadoSocketC('1')  # Indica que el socket C esta activo


        else:
            contador += 1
            sys.stdout.write("*")
            sys.stdout.flush()
            class_db.estadoSocketC('0')
            if contador == maxIntentos:
                print "REINICIO AUTOMATICO DEL  SOCKET"
                logger.warning("Reinicio Automatico del Monedero")
                InhibirMDB.main()
                try:
                    iniciarThread()
                    contador = 0
                except:
                    class_db.estadoSocketC('0')



# -------------------------- FUNCIONES  --------------------------------------------

def hacerCorteAutomatico():
    global BANDERA_CORTE
    global CONTADOR_CORTE
    if BANDERA_CORTE:
        hacerCorte = False
        banderaTiempo = class_db.consultarTipoTiempo()
        if banderaTiempo == "cadaDia":
            horaCorte = str(class_db.consultarTiempo())
            horaActual = libgral.ObtenerHora()
	    horaCorte = datetime.strptime(horaCorte, '%H:%M:%S')
	    horaCorte = str(horaCorte).split(' ')
	    horaCorte = str(horaCorte[1])
            if horaCorte == horaActual:
                hacerCorte = True

        if banderaTiempo == "cadaSemana":
            diaHora = class_db.consultarTiempo()
            diaHora = diaHora.split('|')
            dia = diaHora[0]
            hora = diaHora[1]
            diaActual = libgral.obtenerNombreDia()
            horaActual = libgral.ObtenerHora()
            if dia == diaActual and hora == horaActual:
                hacerCorte = True

        if banderaTiempo == "cadaMes":
            diaHora = class_db.consultarTiempo()
            diaHora = diaHora.split('|')
            dia = diaHora[0]
            hora = diaHora[1]
            diaActual = libgral.obtenerDia()
            horaActual = libgral.ObtenerHora()
            if dia == diaActual and hora == horaActual:
                hacerCorte = True

        if banderaTiempo == "cadaDetHora":
            hora = class_db.consultProxCorte()
            hora  = hora[:-3]
            horaActual = libgral.ObtenerHora()
            hora2 = class_db.consultarTiempo()
            horaActual = horaActual[:-3]
            if hora == horaActual:
                hacerCorte = True
                proxCorte = libgral.generarProximoCorte(hora2)
                class_db.registroProxCorteAuto(proxCorte)
        if hacerCorte:
            if DEBUG:
                print "CORTE DE TURNO AUTOMATICO"
            class_db.activarCorteTurno()
            #global BANDERA_CORTE 
            BANDERA_CORTE = False
    else:
        #global CONTADOR_CORTE 
        CONTADOR_CORTE += 1
    if CONTADOR_CORTE == 6:
        #global BANDERA_CORTE 
        BANDERA_CORTE = True
	CONTADOR_CORTE = 0



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
    if DEBUG:
        print "Tx: " + ultimoTicket
    return ultimoTicket


def cambiarTarifa():
    nuevaTarifa = class_db.tarifa()  # Consulta la tarifa de la configuracion
    nuevaTarifa = int(nuevaTarifa * 100)
    if nuevaTarifa != tarifaActual:  # Si hay cambio de tarifa retorna True para mandar la nueva tarifa
        if DEBUG:
            print "*" * 40
            print "Nueva Tarifa : ", nuevaTarifa
            print "Antigua Tarifa : ", tarifaActual
            print "*" * 40
        return True
    else:
        return False


def cambiarTiempoA():
    nuevoTiempo = class_db.tiempo_apertura()
    if str(nuevoTiempo) != str(tiempoActual):
        if DEBUG:
            print '*' * 40
            print "ANTIGUO TIEMPO: ", tiempoActual
            print "NUEVO TIEMPO: ", nuevoTiempo
            print '*' * 40
        return True
    else:
        return False


def hacerCorteTurno():
    return class_db.consultarCorteTurno()


def cambiarCanalesHopper():
    return class_db.hayCambiosMonedero()


def estadoCanales():
    mensaje = "C|h"
    estados = class_db.canales_monedero()
    estados = estados
    for estado in estados:
	mensaje += str(estado[1])
    if DEBUG:
	print "TX: ", mensaje
    return mensaje


def totalMonto(entrada):
    total = 0
    arreglo = entrada.split(';')
    monedero = arreglo[0].split(',')
    billetero = arreglo[1].split(',')
    totalMonedeo = int(monedero[1])
    totalBilletero = int(billetero[1])
    total = totalMonedeo + totalBilletero
    total = total / 100
    if DEBUG:
        print "RX: ", total
    return total



if __name__ == '__main__':
    """
    time.sleep(0.100)
    try:
        iniciarThread()
    except (KeyboardInterrupt, SystemExit):
        if DEBUG:
            print "REGISTRANDO EL ESTADO DEL SOCKET DE C EN INACTIVO"
        class_db.estadoSocketC('0')
    """
    try:
        Socket()
    except KeyboardInterrupt:
        if DEBUG:
            print "REGISTRANDO EL ESTADO DEL SOCKET DE PYTHON EN INACTIVO"
        class_db.estadoSocketPython('0')

