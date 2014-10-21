#-*- coding: utf-8 -*-

import flask
from flask import redirect, session, url_for, request


class Logout(flask.views.MethodView):
	def post(self):
		bandera = request.form['submit']
		if bandera == 'salir':
			vista = request.form['vista']
			session.clear()
			if vista == "home":
				return redirect(url_for('home'))
			elif vista == "estadoSistema":
				return redirect(url_for('estadoSistema'))