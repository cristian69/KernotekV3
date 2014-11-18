# -*- coding: utf-8 -*-
import flask
from flask import render_template, redirect, url_for, session, request
import class_db
import libgral
import time

class Turnos(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			typeCut = class_db.tipoCorte()
			return render_template('corteDeTurno.html', tipoCorte=typeCut)
		else:
			return redirect(url_for('login'))

	def post(self):
		stateC, statePython = libgral.revisarProceso()
		typeCut = class_db.tipoCorte()
		option = request.form.getlist('seleccionarAccion2')
		option = option[0]
		bandera = ""
		# print "Option: ", option
		if option == "cambiar":
			typeCut = request.form.getlist('tiposCortes2')
			typeCut = typeCut[0]
			if typeCut == 'automatico':
				typeCut = '1'
			else:
				typeCut = '0'

			if typeCut is not "1":
				class_db.cambiarTipoCorte(typeCut)
				typeCut = class_db.tipoCorte()
				return render_template('corteDeTurno.html', bandera="cambioTipoCorte", tipoCorte=typeCut)
			else:
				option = "configurar"

		if option == "configurar":
			typeLapse = request.form.getlist('tipoLapso')
			typeLapse = typeLapse[0]
			if typeLapse == "cadaDia":
				timeAutoCut = request.form['hora']
				class_db.registroProxCorteAuto("")
			if typeLapse == "cadaSemana":
				dayWeek = request.form.getlist('diaSem')
				dayWeek = dayWeek[0]
				timeCut = request.form['hora']
				timeAutoCut = dayWeek + '|' + timeCut
				class_db.registroProxCorteAuto("")
			if typeLapse == 'cadaMes':
				dayMonth = request.form.getlist('diaMes')
				dayMonth = dayMonth[0]
				timeCut = request.form['hora']
				timeAutoCut = dayMonth + '|' + timeCut
				class_db.registroProxCorteAuto("")
			if typeLapse == 'cadaDetHora':
				timeAutoCut = request.form['hora']
				nextCut = libgral.generarProximoCorte(timeAutoCut)
				class_db.registroProxCorteAuto(nextCut)

			bandera = "configuracionExitosa"
			class_db.cambiarTipoCorte('1')
			class_db.tipoTiempoAutomatico(typeLapse)
			class_db.tiempoCorteAuto(timeAutoCut)	
			return render_template('corteDeTurno.html', bandera=bandera, tipoCorte=typeCut)

		if option == "corte":
			class_db.activarCorteTurno()
			time.sleep(2)  # Espera a que el corte de turno se ejecute
			bandera = "corteExitoso"

		return render_template('corteDeTurno.html', bandera=bandera)