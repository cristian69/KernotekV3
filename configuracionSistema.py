#-*- conding: utf-8 -*-
import flask
from flask import render_template, redirect, session, request, url_for
import class_db

class Configuracion(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			return render_template('configuracionSistema.html')

		else:
			return redirect(url_for('login'))

	def post(self):
		pass