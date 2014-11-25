#-*- conding: utf-8 -*-
import flask
from flask import render_template, redirect, session, request, url_for
import class_db
from estado_sistema import sistema
import config_sistema
class Configuracion(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			stateSystem = sistema()
			botonSystem = config_sistema.estadoSistema()
			return render_template('configuracionSistema.html', estado_sistema = stateSystem, botonSistema=botonSystem)

		else:
			return redirect(url_for('login'))

	def post(self):
		pass