# -*- coding: utf-8 -*-
import flask
from flask import render_template, redirect, url_for, session, request
import class_db


class Turnos(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			return render_template('corteDeTurno.html')

	def post():
		pass