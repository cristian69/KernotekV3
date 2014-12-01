#-*- conding: utf-8 -*-
import flask
from flask import render_template, redirect, session, request, url_for
import classdb
from libgral import terminarProceso, revisarProceso, iniciarProceso, reiniciarProceso
import inhibirMDB
import time

RESTART = "reiniciar"
START = "iniciar"
STOP = "detener"


class Configuracion(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			stateSystem = sistema()
			botonSystem = revisarProceso()
			return render_template('configuracionSistema.html', estado_sistema = stateSystem, botonSistema=botonSystem)

		else:
			return redirect(url_for('login'))

	def post(self):
		operation = request.form['submit']
		if operation == STOP:
			terminarProceso()
			InhibirMDB.main()
		elif operation == START:
			iniciarProceso()
			time.sleep(1)	
		elif operation == RESTART:
			reiniciarProceso()
		else:
			return redirect(url_for('login'))
		time.sleep(1)	
		stateSystem = sistema()
		botonSystem = configsistema.estadoSistema()
		return render_template('configuracionSistema.html', estado_sistema = stateSystem, botonSistema=botonSystem)		


def cambioSistema():
    numSerie = request.form['numSerie']
    tarifa = request.form['tarifa']
    tiempoApertura = request.form['tiempoApertura']
    monederoSerie = request.form['monederoSerie']
    billeteroSerie = request.form['billeteroSerie']
    cambiar_estado_sistema(numSerie, tarifa, tiempoApertura, billeteroSerie, monederoSerie)


def sistema():
    data = classdb.estado_sistema()
    datos_sistema = {'numSerie': '',
                    'rate':'',
                    't_apertura':'',
                    'ticket_actual':0,
                    'turno':0,
                    'num_payout':'',
                    'num_hopper':''}

    datos_sistema['numSerie'] = data[0]
    datos_sistema['rate'] =str(data[1]) + "0"
    datos_sistema['t_apertura'] = str(data[2])
    datos_sistema['ticket_actual'] = data[3]
    datos_sistema['turno'] = data[4]
    datos_sistema['num_payout'] = data[5]
    datos_sistema['num_hopper'] = data[6]
    return datos_sistema
