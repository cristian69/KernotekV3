# -*- coding:utf-8 -*-
__author__ = 'jbadillo'
__author__ = 'aramirez'

################################################
#                                              #
#   Clase para el apagado y prendido de luces  #
#                                              #
################################################

import socket

INITIAL_MODBUS = 0xFFFF
INITIAL_DF1 = 0x0000

__FOCO1__ = "1"
__FOCO2__ = "2"
__FOCO3__ = "3"
__FOCO4__ = "4"
__FOCO5__ = "5"
__FOCO6__ = "6"
__FOCO7__ = "7"
__FOCO8__ = "8"

__PRENDER__ = "1"
__APAGAR__ = "2"
__ESTADO__ = "3"
__SALIR__ = "4"

RELAY01_ON  = "\x01\x06\x00\x00\x00\x01\x48\x0A"
RELAY01_OFF = "\x01\x05\x00\x00\x00\x00\xCD\xCA"
RELAY02_ON  = "\x01\x06\x00\x01\x00\x01\x19\xCA"
RELAY02_OFF = "\x01\x05\x00\x01\x00\x00\x9C\x0A"
RELAY03_ON  = "\x01\x06\x00\x02\x00\x01\xE9\xCA"
RELAY03_OFF = "\x01\x05\x00\x02\x00\x00\x6C\x0A"
RELAY04_ON  = "\x01\x06\x00\x03\x00\x01\xB8\x0A"
RELAY04_OFF = "\x01\x05\x00\x03\x00\x00\x8C\x0B"
RELAY05_ON  = "\x01\x06\x00\x04\x00\x01\x09\xCB"
RELAY05_OFF = "\x01\x05\x00\x04\x00\x00\xFF\x6A"
RELAY06_ON  = "\x01\x06\x00\x05\x00\x01\x58\x0B"
RELAY06_OFF = "\x01\x05\x00\x05\x00\x00\xDD\xCB"
RELAY07_ON  = "\x01\x06\x00\x06\x00\x01\xA8\x0B"
RELAY07_OFF = "\x01\x05\x00\x06\x00\x00\x2D\xCB"
RELAY08_ON  = "\x01\x06\x00\x07\x00\x01\xF9\xCB"
RELAY08_OFF = "\x01\x05\x00\x07\x00\x00\x7C\x0B"

RELAY_STATUS = "\x01\x01\x00\x00\x00\x08\xBD\xC1"

TCP_IP = '192.168.0.88'
TCP_PORT = 8080
BUFFER_SIZE = 1024


def control(luz):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(RELAY03_ON)
    data = s.recv(BUFFER_SIZE)
    print data


def main():
    print '=' * 40
    print "Ingresa la opracion que deseas : \n1.-ENCENDER UNA LUZ.\n2.-APAGAR UNA LUZ.\n3.-VER ESTADO.\n4.-Salir "
    operacion = raw_input(">> ")
    if operacion == __PRENDER__ :
        prender_luz()
    elif operacion == __APAGAR__ :
        apagar_luz()
    elif operacion == __ESTADO__:
        estado()
    elif operacion ==__SALIR__:
        print "Adios"
        exit(04)
    else:
        print "NO es una opcion intenta nuevamente"
        main()

def estado():
    print "El estado de las luces es: "
    control(RELAY_STATUS)

def prender_luz():
    print "Elige la el foco que quieres prender: \nDisponibles del 1-8.\n\nPresiona 9 y enter para regresar"
    prender = raw_input(">> ")
    if prender == __FOCO1__:
        print "Foco 1 prendido"
        control(RELAY01_ON)
    elif prender == __FOCO2__:
        print "Foco 2 prendido"
        control(RELAY02_ON)
    elif prender == __FOCO3__:
        print "Foco 3 prendido"
        control(RELAY03_ON)
    elif prender == __FOCO4__:
        print "Foco 4 prendido"
        control(RELAY04_ON)
    elif prender == __FOCO5__:
        print "Foco 5 prendido"
        control(RELAY05_ON)
    elif prender == __FOCO6__:
        print "Foco 6 prendido"
        control(RELAY06_ON)
    elif prender == __FOCO7__:
        print "Foco 7 prendido"
        control(RELAY07_ON)
    elif prender == __FOCO8__:
        print "Foco 8 prendido"
        control(RELAY08_ON)
    elif prender == "9":
        main()
    else:
        print "No esta disponible esa opcion, intenta otra"
        prender_luz()

def apagar_luz():
    print "Elige la el foco que quieres apagar: \nDisponibles del 1-8.\n\nPresiona 9 y enter para regresar"
    apagar = raw_input(">> ")
    if apagar == __FOCO1__:
        print "Foco 1 apagado"
        control(RELAY01_OFF)
    elif apagar == __FOCO2__:
        print "Foco 2 apagado"
        control(RELAY02_OFF)
    elif apagar == __FOCO3__:
        print "Foco 3 apagado"
        control(RELAY03_OFF)
    elif apagar == __FOCO4__:
        print "Foco 4 prendido"
        control(RELAY04_OFF)
    elif apagar == __FOCO5__:
        print "Foco 5 apagado"
        control(RELAY05_OFF)
    elif apagar == __FOCO6__:
        print "Foco 6 apagado"
        control(RELAY06_OFF)
    elif apagar == __FOCO7__:
        print "Foco 7 prendido"
        control(RELAY07_OFF)
    elif apagar == __FOCO8__:
        print "Foco 8 prendido"
        control(RELAY08_OFF)
    elif apagar == "9":
        main()
    else:
        print "No esta disponible esa opcion, intenta otra"
        apagar_luz()
main()
