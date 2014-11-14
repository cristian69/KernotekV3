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
from reporte_especifico import cod_tabla

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
	    typeGrafic = request.args.get('grafica')
	    if typeGrafic == "diaria" or typeGrafic == "None":
		dayGrafic, sells = graficaDia()
		return render_template('home.html', dic_home=dic_home, dias=dayGrafic, valoresDia=sells, bandera="graficaDia")
	    elif typeGrafic == "semanal":
		weekGrafic, sells = graficaSemana()
		return render_template('home.html', dic_home=dic_home, semanas=weekGrafic, valoresSemana=sells, bandera="graficaSemana")
            else:
		monthGrafic, sells = graficaMes()
	    	return render_template('home.html',dic_home=dic_home, meses=monthGrafic, valoresMes=sells, bandera="graficaMes")
        else:
            ip = request.remote_addr
            logger.seguridad('INTENTO DE BURLAR LA SEGURIDAD| IP RESPONSABLE: ' + ip)
            return redirect(url_for('login'))

    def post(self):
        operation = request.form['submit']
        flag = ""
        print operation
        if operation == REPORT:
            typeReport = request.form.getlist('tipoReporte')
            typeReport = typeReport[0]
            startDate = request.form['fecha_inicio'] + ' ' + request.form['hora_inicio']
            endDate = request.form['fecha_fin'] + ' ' + request.form['hora_fin']
            if typeReport == SHIFT_REPORT:
                codeShift = turnosDisponibles
                return render_template('reportesTurno.html')
            if typeReport == DATES_REPORT:
                indexHTML = numeracion_paginas(startDate, endDate, 1, 0, 'reportes')
                tableHTML = cod_tabla(startDate, endDate, 0)
                if len(tableHTML) == 66:
                    return render_template('reporteFechas.html', tableHTML=tableHTML, bandera=1)
                else:
                    return render_template('reporteFechas.html', tableHTML=tableHTML, indexHTML=indexHTML, bandera=1)

        if operation == CHANGE_RATE:
            newRate = request.form['nuevaTarifa']
            class_db.cambiarTarifa(newRate)
            flag = "tarifaExitosa"

        if operation == CHANGE_TIME_OPEN:
            newTime = request.form['nuevoTiempo']
            class_db.cambiarTiempoApertura(newTime)
            flag = "tiempoExitoso"

        if operation == CUT_SHIFT:
            class_db.activarCorteTurno()
            time.sleep(2)  # Espera a que el corte de turno se ejecute
            flag = "corteExitoso"

        dic_home = datos_home()
        # return render_template('reporteFechas.html')
        return render_template('home.html',dic_home=dic_home, bandera=flag)


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
    for i in range(0,7):
	m = datetime.datetime(2014,mesActual,1)
	try:
	    mes = datos[i]
	except:
	    mes = [0,0]
        if int(mes[0]) == int(mesActual):
            listaMeses.append(nombreMes(str(m.strftime('%b'))))
            listaVentas.append(mes[1])
        else:
            listaMeses.append(nombreMes(str(m.strftime('%b'))))
            listaVentas.append(float('0.0'))
        mesActual -= 1
        if mesActual == 0:
            mesActual = 12

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
    for i in range(0,7):
	try:
	    semana = datos[i]
	except:
	    semana = [0,0]
        if int(semana[0]) == int(semanaActual):
            listaSemanas.append(inicioSemana(year, semanaActual + 1))
            listaVentas.append(semana[1])
        else:
            listaSemanas.append(inicioSemana(year, semanaActual + 1))
            listaVentas.append(float(0))

        semanaActual -= 1
        if semanaActual == 0:
            semanaActual = 51
            year -= 1

    semanas = []
    ventas = []

    for indice in range(len(listaSemanas)-1, -1, -1):
        ventas.append(listaVentas[indice])
        semanas.append(listaSemanas[indice])

    return semanas, ventas

def graficaDia():
    datos = class_db.ventasDia()
    print datos
    fecha = str(ObtenerFecha()).split('-')
    year = int(fecha[0])
    mes = int(fecha[1])
    ultimoDia = monthrange(year,mes)
    ultimoDia = int(ultimoDia[1])
    diaActual = int(obtenerDia())
    listaDias = []
    listaVentas = []
    listaPrueba = []
    for x in range(7):
	try:
	    dia = datos[x]
	except:
	    dia = [diaActual, 0]
	lista = []
	print dia[0], diaActual - x
	if int(dia[0]) == diaActual - x:
	    listaPrueba.append(dia)
	else:
	    lista = [diaActual, 0]
	    listaPrueba.append(lista)
	diaActual -= 1
    
    diaActual = int(obtenerDia())
    for i in range(7):
        try:
	    dia = datos[i]
	except:
	    dia = [0,0]
        if int(dia[0]) == int(diaActual) - i:
            d = datetime.datetime(year, mes, diaActual)
            listaDias.append( nombreMes(str(d.strftime('%b'))) + " "+str(d.strftime('%d')) )
            listaVentas.append(float(dia[1]))
        else:
            d = datetime.datetime(year, mes, diaActual)
            listaDias.append( nombreMes(str(d.strftime('%b'))) + " "+str(d.strftime('%d')) )
            listaVentas.append(float(0))

        diaActual -= 1
        if diaActual == 0:
            fecha = str(ObtenerFecha()).split('-')
            year = int(fecha[0])
            mes = int(fecha[1]) - 1
            if mes == 0:
                mes = 12
                year -= 1
            ultimoDia = monthrange(year,mes)
            diaActual = int(ultimoDia[1])
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


