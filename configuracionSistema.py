#-*- conding: utf-8 -*-
import flask
from flask import render_template, redirect, session, request, url_for
import class_db
from estado_sistema import sistema
import config_sistema
from libgral import terminarProceso, revisarProceso, iniciarProceso, reiniciarProceso
import InhibirMDB
import time

RESTART = "reiniciar"
START = "iniciar"
STOP = "detener"


class Configuracion(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			stateSystem = sistema()
			botonSystem = config_sistema.estadoSistema()
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
		elif operation == RESTART:
			reiniciarProceso()
		else:
			return redirect(url_for('login'))
		time.sleep(0.5)	
		stateSystem = sistema()
		botonSystem = config_sistema.estadoSistema()
		return render_template('configuracionSistema.html', estado_sistema = stateSystem, botonSistema=botonSystem)		