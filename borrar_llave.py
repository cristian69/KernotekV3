# -*- coding: utf-8 -*-

import flask
from flask import render_template, request, redirect, session, url_for
from class_db import eliminarLlave

class borrarLlave(flask.views.MethodView):
	def post(self):
		codigoLlave= request.form['codigLlave']
		eliminarLlave(codigoLlave)
		return render_template('llavesEditar.html')
