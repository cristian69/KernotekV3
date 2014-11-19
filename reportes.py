# -*- coding:utf-8 -*-

import flask
from flask import render_template, redirect, url_for, session, request
import class_db
from libgral import numeracion_paginas
from reporte_especifico import cod_tabla
from reporte_general import tablaReporte
import excel

NONE = 66
class Reportes(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			typeReport = ""
			typeReport = request.args.get('reporte')
			startDate = request.args.get('fecha1')
			endDate = request.args.get('fecha2')
			index = str(request.args.get('indice'))
			actualPage = str(request.args.get('num_pagina'))
			objExcel = excel
			flagTableDate = True
			if typeReport == "detallado":
				sellsReport = class_db.reportDetallado(startDate, endDate)
				excel.reporteDetallado(sellsReport, startDate, endDate)
				return render_template('reporteFechas.html', indexHTML="", tableHTML="", bandera=0, tablaFechas=flagTableDate, excel=True)
			if typeReport == "especifico":
				indexHTML = numeracion_paginas(startDate, endDate, 1, 0, 'reportes')
				tableHTML = cod_tabla(startDate, endDate, 0)
				return render_template('reporteFechas.html', indexHTML=indexHTML, tableHTML=tableHTML, tablaFechas=flagTableDate, excel=False)
			
			if typeReport == "generarEspecifico":
				sellsReport = class_db.reporte_especifico(startDate, endDate)
				objExcel.export_excel(sellsReport, startDate, endDate)
				indexHTML = numeracion_paginas(startDate, endDate, 1, 0, 'reportes')
				tableHTML = cod_tabla(startDate, endDate, 0)
				return render_template('reporteFechas.html', indexHTML=indexHTML, tableHTML=tableHTML, tablaFechas=flagTableDate, excel=True)

			if typeReport == "general":
				sells = class_db.reporte_general(startDate, endDate)
				tableHTML = tablaReporte(sells, startDate, endDate)
				return render_template('reporteFechas.html', tableHTML=tableHTML, tablaFechas=flagTableDate, excel=False)

			if typeReport == "generarGeneral":
				sellsReport = class_db.reporte_general(startDate, endDate)
				objExcel.reporteGeneral(sellsReport, startDate, endDate)
				tableHTML = tablaReporte(sellsReport, startDate, endDate)
				return render_template('reporteFechas.html', tableHTML=tableHTML, tablaFechas=flagTableDate, excel=True)
			
			if index != 'None' and startDate != 'None' and endDate != 'None':
				indexHTML = numeracion_paginas(startDate, endDate, actualPage, index,'reportes')
				tableHTML = cod_tabla(startDate, endDate, index)
				return render_template('reporteFechas.html', indexHTML=indexHTML, tableHTML=tableHTML, tablaFechas=flagTableDate)
			else:
				flagTableDate = False
				return render_template('reporteFechas.html', indexHTML="", tableHTML="", bandera=0, tablaFechas=flagTableDate)
		else:
			return redirect(url_for('login'))

	def post(self):
		startDate = request.form['fecha_inicio'] + ' ' + request.form['hora_inicio']
		endDate = request.form['fecha_fin'] + ' ' + request.form['hora_fin']
		sells = class_db.reporte_general(startDate, endDate)
		tableHTML = tablaReporte(sells, startDate, endDate)
		if len(tableHTML) == 75:
			return render_template('reporteFechas.html', tableHTML=tableHTML, tablaFechas=False, excel=False)
		else:
			return render_template('reporteFechas.html', tableHTML=tableHTML,  tablaFechas=True, excel=False)
		"""
		indexHTML = numeracion_paginas(startDate, endDate, 1, 0, 'reportes')
		tableHTML = cod_tabla(startDate, endDate, 0)
		if len(tableHTML) == NONE:
			return render_template('reporteFechas.html', tableHTML=tableHTML, indexHTML="")
		return render_template('reporteFechas.html', tableHTML=tableHTML, indexHTML=indexHTML)
		"""    
