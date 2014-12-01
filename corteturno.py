#-*- coding: utf-8 -*-

__autor__ = 'aramirez'

import flask
from flask import render_template, redirect, session, url_for, request
import classdb
import time
import libgral

class corteTurno(flask.views.MethodView):
	def get(self):
		if len(session) > 1:
			dicTurno = datosTurno()
			return render_template('corteTurno.html', dicTurno=dicTurno);
		else:
			return redirect(url_for('login'));

	def post(self):
		socketPython = class_db.consultaSocketPython()
		socketC = class_db.consultaSocketC()
		if socketPython == 'Activo' and socketC == 'Activo':
			bandera = request.form['submit']
			if bandera == "hacerCorte":
				class_db.activarCorteTurno()
				time.sleep(2)  # Espera a que el corte de turno se ejecute
				dicTurno = datosTurno()
				bandera = "corteExitoso"
				
			if bandera == "aceptarTipoCorte":
				tipoCorte = request.form['tipoCorte']
				class_db.cambiarTipoCorte(tipoCorte)
				dicTurno = datosTurno()
				bandera = "cambioExitoso"

			if bandera == 'tiempoCorteAutomatico':

				#tipoCorte = request.form['tipoCorte']
				#print tipoCorte
				class_db.cambiarTipoCorte('1')
				dicTurno = datosTurno()

				tipoLapso = request.form.getlist('tipoLapso')
				tipoLapso = tipoLapso[0]
				tiempo = ""
				proxCorte = ""
				bandera = "configuracionExitosa"

				if tipoLapso == 'cadaDia':
					hora = request.form['hora']
					tiempo = str(hora)
					class_db.registroProxCorteAuto("")
				elif tipoLapso == 'cadaSemana':
					diaSem = request.form.getlist('diaSem')
					diaSem =  diaSem[0]
					hora = request.form['hora']
					tiempo = diaSem + "|" + str(hora)
					class_db.registroProxCorteAuto("")
				elif tipoLapso == 'cadaMes':
					diaMes = request.form.getlist('diaMes')
					diaMes = diaMes[0]
					hora = request.form['hora']
					tiempo = str(diaMes) + "|" + str(hora)
					class_db.registroProxCorteAuto("")
				elif tipoLapso == 'cadaDetHora':
					hora = request.form['hora']
					tiempo = str(hora)
					proxCorte = libgral.generarProximoCorte(tiempo)
					class_db.registroProxCorteAuto(proxCorte)
				
				class_db.tipoTiempoAutomatico(tipoLapso)
				class_db.tiempoCorteAuto(tiempo)
				

			dicTurno = datosTurno()
			return render_template('corteTurno.html', dicTurno = dicTurno, bandera = bandera)
		else:
			dicTurno = datosTurno()
			return render_template('corteTurno.html', bandera = "noDisponible", dicTurno = dicTurno)


# Regresa un diccionario con los datos del turno actual
def datosTurno():
	dicTurno = {'noTurno':0,
				'fechaInicio': "",
				'horaInicio':"",
				'ventasTurno': 0,
				'tipoCorte': '',
				'tipoLapso': '',
				'diaCorte': '',
				'horaCorte': '',
				'estadoManual':'',
				'estadoAutomatico': ''}

	tipoLapso = str(class_db.consultarTipoTiempo())
	
	if tipoLapso == 'cadaDia':
		dicTurno['horaCorte'] = str(class_db.consultarTiempo())
		
	elif tipoLapso == 'cadaSemana':
		diaHora = str(class_db.consultarTiempo())
		diaHora = diaHora.split('|')
		dicTurno['diaCorte'] = diaHora[0]
		dicTurno['horaCorte'] = diaHora[1]
	elif tipoLapso == 'cadaMes':
		diaMes = str(class_db.consultarTiempo())
		diaMes = diaMes.split('|')
		dicTurno['diaCorte'] = diaMes[0]
		dicTurno['horaCorte'] = diaMes[1]
	elif tipoLapso == 'cadaDetHora':
		dicTurno['horaCorte'] = str(class_db.consultarTiempo())
		

	dicTurno['tipoLapso'] = tipoLapso
	datosConsulta = class_db.datosTurnoActual()
	fechaHora = str(datosConsulta[1]).split(" ")
	fecha = fechaHora[0] + "  "
	hora =  fechaHora[1] + " Hrs."
	dicTurno['noTurno'] = str(datosConsulta[0])
	dicTurno['fechaInicio'] = fecha
	dicTurno['horaInicio'] = hora
	dicTurno['ventasTurno'] = str(class_db.ventasTurno(dicTurno['noTurno']))  # Contiene las ventas de el turno activo
	dicTurno['tipoCorte'] = class_db.tipoCorte()
	if dicTurno['tipoCorte'] == 'manual':
		dicTurno['estadoManual'] = 'checked'
	else:
		dicTurno['estadoAutomatico'] = 'checked'

	#print dicTurno
		
	return dicTurno
	

