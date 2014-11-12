# -*- coding:utf-8 -*-

import flask
from flask import render_template, redirect, url_for, session, request
import class_db
from libgral import numeracion_paginas
from reporte_especifico import cod_tabla


class Reportes(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			index = str(request.args.get('indice'))
			startDate = str(request.args.get('fecha1'))
			endDate = str(request.args.get('fecha2'))
			actualPage = str(request.args.get('num_pagina'))
			if index != 'None' and startDate != 'None' and endDate != 'None':
				indexHTML = numeracion_paginas(startDate, endDate, actualPage, index,'reportes')
				tableHTML = cod_tabla(startDate, endDate, index)
				return render_template('reporteFechas.html', indexHTML=indexHTML, tableHTML=tableHTML)
			else:
				return render_template('reporteFechas.html', indexHTML="", tableHTML="", bandera=0)
		else:
			return redirect(url_for('login'))

	def post(self):
		pass