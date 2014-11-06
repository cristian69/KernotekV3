#-*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import render_template, redirect, session, request, url_for
from estado_sistema import monedero, billetero, sistema
from class_db import cambiar_estado_sistema
import class_db
from libgral import terminarProceso, revisarProceso, iniciarProceso, reiniciarProceso
import InhibirMDB
import time


DETENER = "False"
ACTIVAR = "True"
REINICIAR = 'Reiniciar'


class ConfigSistema(flask.views.MethodView):
    def post(self):
        socketPython = class_db.consultaSocketPython()
        socketC = class_db.consultaSocketC()
        if socketPython == 'Activo' and socketC == 'Activo':
            bandera = request.form['submit']
            if bandera == 'cambioSistema':
                cambioSistema()
                datos_sistema = sistema()
                estado_monedero = monedero()
                estado_billetero = billetero()
                botonSistema = estadoSistema()
                return render_template('Config_sistema.html',
                                       datos_sistema=datos_sistema,
                                       estado_monedero=estado_monedero,
                                       estado_billetero=estado_billetero,
                                       botonSistema= botonSistema)
            elif bandera == 'cambioMonedero':
                cambioMonedero()
                datos_sistema = sistema()
                estado_monedero = monedero()
                estado_billetero = billetero()
                botonSistema = estadoSistema()
                return render_template('Config_sistema.html',
                                       datos_sistema=datos_sistema,
                                       estado_monedero=estado_monedero,
                                       estado_billetero=estado_billetero,
                                       botonSistema= botonSistema)
            elif bandera == 'cambioBilletero':
                cambioBilletero()
                datos_sistema = sistema()
                estado_monedero = monedero()
                estado_billetero = billetero()
                botonSistema = estadoSistema()
                return render_template('Config_sistema.html',
                                       datos_sistema=datos_sistema,
                                       estado_monedero=estado_monedero,
                                       estado_billetero=estado_billetero,
                                       botonSistema= botonSistema)
            elif bandera == "botonSistema":
                estadoBoton = request.form['btnSistema']
                if estadoBoton == DETENER:
                    terminarProceso()
                    InhibirMDB.main()
                elif estadoBoton == ACTIVAR:
                    iniciarProceso()
                elif estadoBoton == REINICIAR:
                    reiniciarProceso()
        
                datos_sistema = sistema()
                estado_monedero = monedero()
                estado_billetero = billetero()
		time.sleep(0.5)
                botonSistema = estadoSistema()
                return render_template('Config_sistema.html',
                                       datos_sistema=datos_sistema,
                                       estado_monedero=estado_monedero,
                                       estado_billetero=estado_billetero,
                                       botonSistema= botonSistema)
            else:
                return redirect(url_for('login'))
        else:
            datos_sistema = sistema()
            estado_monedero = monedero()
            estado_billetero = billetero()
            botonSistema = estadoSistema()
            return render_template('Config_sistema.html',
                                   datos_sistema=datos_sistema,
                                   estado_monedero=estado_monedero,
                                   estado_billetero=estado_billetero,
                                   bandera = "noDisponible",
                                   botonSistema= botonSistema)

    def get(self):
        if len(session) > 1:
            datos_sistema = sistema()
            estado_monedero = monedero()
            estado_billetero = billetero()
            botonSistema = estadoSistema()
            return render_template('Config_sistema.html',
                                   datos_sistema=datos_sistema,
                                   estado_monedero=estado_monedero,
                                   estado_billetero=estado_billetero,
                                   botonSistema= botonSistema)
        else:
            return redirect(url_for('login'))


def estadoSistema():
    python, C = revisarProceso()
    if python and C:
        return True
    return False

def cambioSistema():
    numSerie = request.form['numSerie']
    tarifa = request.form['tarifa']
    tiempoApertura = request.form['tiempoApertura']
    monederoSerie = request.form['monederoSerie']
    billeteroSerie = request.form['billeteroSerie']
    cambiar_estado_sistema(numSerie, tarifa, tiempoApertura, billeteroSerie, monederoSerie)


# regresa el estado de cada canal del monedero
def cambioMonedero():
    m10 = request.form['m10']
    m5 = request.form['m5']
    m2 = request.form['m2']
    m1 = request.form['m1']
    m05 = request.form['m05']
    class_db.cambioMonedero(m05, m1, m2, m5, m10)


# Regresa el estado de cada canal del billetero
def cambioBilletero():
    b20 = request.form['b20']
    b50 = request.form['b50']
    b100 = request.form['b100']
    b200 = request.form['b200']
    b500 = request.form['b500']
    class_db.cambioBilletero(b20, b50, b100, b200, b500)
