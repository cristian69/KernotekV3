# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import render_template, redirect, url_for, session, request
import class_db
from libgral import numeracion_paginas, ObtenerFecha, revisarProceso, obtenerDia, obtenerNombreDia, nombreMes, nombreDias
import logger
import time 
import datetime 
from calendar import monthrange
from datetime import date, timedelta
from reporteTurno import turnosDisponibles
from libgral import numeracion_paginas
from reporte_general import tablaReporte


REPORT = "reporte"
SHIFT_REPORT = "turno"
DATES_REPORT = "fechas"
CHANGE_RATE = "tarifa"
CHANGE_TIME_OPEN = "tiempoApertura"
CUT_SHIFT = "aceptarCorte"


class Home(flask.views.MethodView):
    def get(self):
        if len(session) > 1:
            dic_home = datos_home()
            typeGrafic = ""
	    typeGrafic = request.args.get('grafica')
	    if typeGrafic == "dia":
		dayGrafic, sells = graficaDia()
		return render_template('home.html', dic_home=dic_home, labels=dayGrafic, datos=sells, bandera="graficaDia")
	    elif typeGrafic == "semana":
		weekGrafic, sells = graficaSemana()
		return render_template('home.html', dic_home=dic_home, labels=weekGrafic, datos=sells, bandera="graficaSemana")
            elif typeGrafic == "mes":
		monthGrafic, sells = graficaMes()
	    	return render_template('home.html',dic_home=dic_home, labels=monthGrafic, datos=sells, bandera="graficaMes")
            else:
                dayGrafic, sells = graficaDia()
                return render_template('home.html', dic_home=dic_home, labels=dayGrafic, datos=sells, bandera="graficaDia")

        else:
            ip = request.remote_addr
            logger.seguridad('INTENTO DE BURLAR LA SEGURIDAD| IP RESPONSABLE: ' + ip)
            return redirect(url_for('login'))

    def post(self):
        operation = request.form['submit']
        flag = ""
        print operation
        stateC, statePython =  revisarProceso()

        if operation == "reporteTurno":
            startDate = request.form['fecha_inicio2'] + ' 00:00:00'
            endDate = request.form['fecha_fin2'] + ' 23:59:59'
            codeShifts = turnosDisponibles(startDate, endDate)
            return render_template('reportesTurno.html', htmlTurnos=codeShifts, tablaTurnos=True)

        if operation == REPORT:
            typeReport = request.form.getlist('tipoReporte')
            typeReport = typeReport[0]
            startDate = request.form['fecha_inicio'] + ' ' + request.form['hora_inicio']
            endDate = request.form['fecha_fin'] + ' ' + request.form['hora_fin']
            if typeReport == SHIFT_REPORT:
                codeShift = turnosDisponibles
                return render_template('reportesTurno.html')
            if typeReport == DATES_REPORT:
                sells = class_db.reporte_general(startDate, endDate)
                tableHTML = tablaReporte(sells,startDate, endDate)

                if len(tableHTML) == 66:
                    return render_template('reporteFechas.html', tableHTML=tableHTML, bandera=1)
                else:
                    return render_template('reporteFechas.html', tableHTML=tableHTML, bandera=1)

        if operation == CHANGE_RATE:
            if stateC and statePython:
                newRate = request.form['nuevaTarifa']
                class_db.cambiarTarifa(newRate)
                flag = "tarifaExitosa"
            else:
                flag = "error"

        if operation == CHANGE_TIME_OPEN:
            if stateC and statePython:
                newTime = request.form['nuevoTiempo']
                class_db.cambiarTiempoApertura(newTime)
                flag = "tiempoExitoso"
            else:
                flag = "error"

        if operation == CUT_SHIFT:
            if stateC and statePython:
                class_db.activarCorteTurno()
                time.sleep(2)  # Espera a que el corte de turno se ejecute
                flag = "corteExitoso"
            else:
                flag = "error"

        dic_home = datos_home()
        dayGrafic, sells = graficaDia()
        return render_template('home.html', dic_home=dic_home, labels=dayGrafic, datos=sells, bandera="graficaDia", operacion=flag)


def inicioSemana(year, numSemana):
    d = date(year, 1 , 1)
    delta_dias = d.isoweekday() - 1
    delta_semanas = numSemana
    if year == d.isocalendar()[0]:
        delta_semanas -= 1
    delta = timedelta(days=-delta_dias, weeks=delta_semanas)
    fecha =  str(d + delta) 
    fecha = fecha.split('-')
    mes = int(fecha[1])
    m =  datetime.datetime(2014, mes, 1)
    mes = m.strftime('%b')
    mes = nombreMes(str(mes))
    dia = int(fecha[2])
    fecha = mes +" "+ str(dia)
    return fecha


def graficaMes():
    datos = class_db.ventasMes()
    mesActual = datetime.date.today()
    mesActual = mesActual.strftime('%m')
    mesActual = int(mesActual)
    listaMeses = []
    listaVentas = []
    listaPibote = []
    for mes in range(7):
	m = [mesActual- mes, 0]
	listaPibote.append(m)
    for mes in listaPibote:
	for d in datos:
	    if int(mes[0]) == int(d[0]):
		mes[1] = float(d[1])
    # Format
    for mes in listaPibote:
	m = datetime.datetime(2014,mes[0],1)
        listaMeses.append(nombreMes(str(m.strftime('%b'))))
        listaVentas.append(mes[1])

    meses = []
    ventas = []
    
    for indice in range(len(listaVentas)- 1, -1, -1):
        ventas.append(listaVentas[indice])
        meses.append(listaMeses[indice])
    
    return meses, ventas

def graficaSemana():
    year = datetime.date.today()
    year = int(year.strftime('%Y'))
	
    semanaActual = int(datetime.date.today().isocalendar()[1]) - 1
    listaSemanas = []
    listaVentas = []
    datos = class_db.ventasSemana()
    semanaActual = int(datetime.date.today().isocalendar()[1]) - 1

    listaPibote = []
    for semana in range(7):
	i = [semanaActual - semana, 0]
	listaPibote.append(i)
    
    for semana in listaPibote:
	for d in datos:
	    if int(semana[0]) == int(d[0]):
		semana[1] = d[1]
    # Format 
    for semana in listaPibote:
	listaSemanas.append(inicioSemana(year, semana[0] + 1))
	listaVentas.append(semana[1])
    semanas = []
    ventas = []

    for indice in range(len(listaSemanas)-1, -1, -1):
        ventas.append(listaVentas[indice])
        semanas.append(listaSemanas[indice])
    
    return semanas, ventas

def graficaDia():
    datos = class_db.ventasDia()
    fecha = str(ObtenerFecha()).split('-')
    year = int(fecha[0])
    mes = int(fecha[1])
    diaActual = int(obtenerDia())
    listaDias = []
    listaVentas = []
    listaPibote = []

    for dia in range(7):
	i = [diaActual - dia, 0]
	listaPibote.append(i)
    
    for dia in listaPibote:
	for x in datos:
	    if int(dia[0]) == int(x[0]):
		dia[1] = int(x[1])

    
    for dia in listaPibote:
	d = datetime.datetime(year,mes, int(dia[0]))
	listaDias.append(str(d.strftime('%b')) +' '+  str(d.strftime('%d')))
	listaVentas.append(float(dia[1]))

    dias = []
    ventas = []
    for indice in range(len(listaDias)-1, -1, -1):
        ventas.append(listaVentas[indice])
        dias.append(str(listaDias[indice]))
   
    return dias, ventas

def datos_home():
    dic_home = {
                't_apertura': int(class_db.tiempo_apertura()), 
                'tarifa': class_db.tarifa(),
                'turno': int(class_db.turnoActual()),
                'tipoCorte': str(class_db.tipoCorte()),
                'valoresMes':'',
                'meses': '',
                'valoresSemana': '',
                'semanas': '',
                'valoresDia': '',
                'dias': '',
                'socketPython': "", 
                'socketC': "",
                'ventasTurno': "",
                'cerradura': class_db.consultarCerradura()
                }

    datosTurno = class_db.datosTurnoActual()
    numTurno = datosTurno[0]

    dic_home['ventasTurno'] = class_db.acumuladoTurno(str(numTurno))

    dic_home['meses'], dic_home['valoresMes'] = graficaMes()
    dic_home['semanas'], dic_home['valoresSemana'] = graficaSemana()
    dic_home['dias'], dic_home['valoresDia'] = graficaDia()


    dic_home['socketPython'], dic_home['socketC'] = revisarProceso()

    if dic_home['socketPython']:
        dic_home['socketPython'] = "Activo"
    else:
        dic_home['socketPython'] = "Desactivo"

    if dic_home['socketC']:
        dic_home['socketC'] = "Activo"
    else:
        dic_home['socketC'] = "Desactivo"

    return dic_home


