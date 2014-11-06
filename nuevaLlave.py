# -*- coding: utf-8 -*-
__autor__="aramirez"

import flask
from flask import render_template, redirect, session, request, url_for
import class_db


class NuevaLlave(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			return render_template('llaveNueva.html')
		else:
			return redirect(url_for('login'))
	def post(self):
		nombre = request.form['nombre']
		apPaterno = request.form['apPaterno']
		apMaterno = request.form['apMaterno']
		grupo = request.form['grupo']
		tipoLlave = request.form.getlist('tipoLlave')
		llave = request.form['llave']
		estado = request.form.getlist('estadoLlave')
		estadoLlave = class_db.existeLlave(llave.upper())
		if not estadoLlave:
			class_db.registroLlave(nombre, apPaterno, apMaterno, grupo, tipoLlave[0], llave.upper(), estado[0])
			return render_template('llaveNueva.html', bandera='registroExitoso')
		else:
			return render_template('llaveNueva.html', bandera='llaveRegistrada')			 