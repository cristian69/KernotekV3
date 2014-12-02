# -*- coding: utf-8 -*-
import flask
from flask import render_template, redirect, url_for, session, request
import classdb
import libgral
import time


class Turnos(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			typeCut = classdb.tipoCorte()
			if typeCut == "manual":
				typeCut = "Manual"
			else:
				typeCut = "Automático"
			dicTurno = valuesAutomaticShift()
			return render_template('corteDeTurno.html', tipoCorte=typeCut, dicTurno=dicTurno)
		else:
			return redirect(url_for('login'))

	def post(self):
		stateC, statePython = libgral.revisarProceso()
		typeCut = classdb.tipoCorte()
		option = request.form['submit']
		dicTurno = valuesAutomaticShift()
		bandera = ""
		if option == "cortemanual":
			classdb.cambiarTipoCorte('0')
			typeCut = classdb.tipoCorte()
			if typeCut == "manual":
				typeCut = "Manual"
			else:
				typeCut = "Automático"
			dicTurno = valuesAutomaticShift()
			return render_template('corteDeTurno.html', bandera="cambioTipoCorte", tipoCorte=typeCut, dicTurno=dicTurno)
		if option == "corteautomatico":
			typeLapse = request.form.getlist('tipoLapso')
			typeLapse = typeLapse[0]
			if typeLapse == "cadaDia":
				timeAutoCut = request.form['hora']
				classdb.registroProxCorteAuto("")
			if typeLapse == "cadaSemana":
				dayWeek = request.form.getlist('diaSem')
				dayWeek = dayWeek[0]
				timeCut = request.form['hora']
				timeAutoCut = dayWeek + '|' + timeCut
				classdb.registroProxCorteAuto("")
			if typeLapse == 'cadaMes':
				dayMonth = request.form.getlist('diaMes')
				dayMonth = dayMonth[0]
				timeCut = request.form['hora']
				timeAutoCut = dayMonth + '|' + timeCut
				classdb.registroProxCorteAuto("")
			if typeLapse == 'cadaDetHora':
				timeAutoCut = request.form['hora']
				nextCut = libgral.generarProximoCorte(timeAutoCut)
				classdb.registroProxCorteAuto(nextCut)

			bandera = "configuracionExitosa"
			classdb.cambiarTipoCorte('1')
			classdb.tipoTiempoAutomatico(typeLapse)
			classdb.tiempoCorteAuto(timeAutoCut)
			dicTurno = valuesAutomaticShift()
			typeCut = classdb.tipoCorte()
			if typeCut == "manual":
				typeCut = "Manual"
			else:
				typeCut = "Automático"
			return render_template('corteDeTurno.html', bandera=bandera, tipoCorte=typeCut, dicTurno=dicTurno)

		if option == "corte":
			if statePython == True and stateC == True:
				classdb.activarCorteTurno()
				time.sleep(4)  # Espera a que el corte de turno se ejecute
				bandera = "corteExitoso"
				return render_template('corteDeTurno.html', bandera="corteturno", tipoCorte=typeCut, dicTurno=dicTurno)
			else:
				bandera="error"
				return render_template('corteDeTurno.html', bandera=bandera, tipoCorte=typeCut, dicTurno= dicTurno)
		return render_template('corteDeTurno.html', bandera=bandera)

def valuesAutomaticShift():
	banderaTiempo = classdb.consultarTipoTiempo()
	dicTurno = {}
	dicTurno['tipoTiempo'] = banderaTiempo
	if banderaTiempo == "cadaDia":
		horaCorte = classdb.consultarTiempo()
		dicTurno['automaticoHora'] = horaCorte
		dicTurno['automaticoDia'] = ""
		dicTurno['tipoTiempo'] = "Diario"
	if banderaTiempo == "cadaSemana":
		diaHora = classdb.consultarTiempo()
		diaHora = diaHora.split('|')
		dicTurno['automaticoDia'] = diaHora[0]
		dicTurno['automaticoHora']= diaHora[1]
		dicTurno['tipoTiempo'] = "Semanal"
	if banderaTiempo == "cadaMes":
		diaHora = classdb.consultarTiempo()
		diaHora = diaHora.split('|')
		dicTurno['automaticoDia'] = diaHora[0]
		dicTurno['automaticoHora']= diaHora[1]
		dicTurno['tipoTiempo'] = "Mensual"

	return dicTurno