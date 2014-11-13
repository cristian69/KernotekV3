# -*- coding: utf-8 -*-
import flask
from flask import render_template, redirect, url_for, session, request
import class_db
import libgral

class Turnos(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			return render_template('corteDeTurno.html')

	def post(self):
		option = request.form.getlist('seleccionarAccion')
		option = option[0]
		if option == "cambiar":
			typeCut = request.form.getlist('tiposCortes')
			typeCut = typeCut[0]
			class_db.cambiarTipoCorte(typeCut)
			return render_template('corteDeTurno.html', bandera="cambioTipoCorte")
		if option == "configurar":
			typeLapse = request.form.getlist('tipoLapso')
			typeLapse = typeLapse[0]
			if typeLapse == "cadaDia":
				timeAutoCut = request.form['hora']
				class_db.registroProxCorteAuto("")
			if typeLapse == "cadaSemana":
				dayWeek = request.form.getlist('diaSem')
				dayWeek = dayWeek[0]
				time = request.form['hora']
				timeAutoCut = dayWeek + '|' + time
				class_db.registroProxCorteAuto("")
			if typeLapse == 'cadaMes':
				dayMonth = request.form.getlist('diaMes')
				dayMonth = dayMonth[0]
				time = request.form['hora']
				timeAutoCut = dayMonth + '|' + time
				class_db.registroProxCorteAuto("")
			if typeLapse == 'cadaDetHora':
				timeAutoCut = request.form['hora']
				nextCut = libgral.generarProximoCorte(timeAutoCut)
				class_db.registroProxCorteAuto(nextCut)

			bandera = "configuracionExitosa"
			class_db.tipoTiempoAutomatico(typeLapse)
			class_db.tiempoCorteAuto(timeAutoCut)	
			return render_template('corteDeTurno.html', bandera=bandera)
		return render_template('corteDeTurno.html')