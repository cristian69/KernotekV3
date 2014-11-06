#-*- coding: utf-8 -*-

import class_db
import libgral




def hacerCorteTurno():
    return class_db.consultarCorteTurno()


def cambiarCanalesHoppper():
    return class_db.hayCambiosMonedero()


def estadoCanales():
    mensaje = "C|h"
    estados = class_db.canales_monedero()
    estados = estados
    for estado in estados:
		mensaje += str(estado[1])
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
    return total



def hacerCorteAutomatico():
    hacerCorte = False
    banderaTiempo = class_db.consultarTipoTiempo()
    if banderaTiempo == "cadaDia":
        horaCorte = class_db.consultarTiempo()
        horaActual = libgral.ObtnerHora()
        if horaCorte == horaActual:
            hacerCorte = True

    if banderaTiempo == "cadaSemana":
        diaHora = class_db.consultarTiempo()
        diaHora = diaHora.split('|')
        dia = diaHora[0]
        hora = diaHora[1]
        diaActual = libgral.obtenerNombreDia()
        horaActual = libgral.ObtnerHora()
        if dia == diaActual and hora == horaActual:
            hacerCorte = True

    if banderaTiempo == "cadaMes":
        diaHora = class_db.consultarTiempo()
        diaHora = diaHora.split('|')
        dia = diaHora[0]
        hora = diaHora[1]
        diaActual = libgral.obtenerDia()
        horaActual = libgral.ObtnerHora()
        if dia == diaActual and hora == horaActual:
            hacerCorte = True

    if banderaTiempo == "cadaDetHora":
        hora = class_db.consultProxCorte()
        hora  = hora[:-3]
        horaActual = libgral.ObtnerHora()
        hora2 = class_db.consultarTiempo()
        horaActual = horaActual[:-3]
        if hora == horaActual:
            hacerCorte = True
            proxCorte = libgral.generarProximoCorte(hora2)
            class_db.registroProxCorteAuto(proxCorte)

    if hacerCorte:
        class_db.activarCorteTurno()