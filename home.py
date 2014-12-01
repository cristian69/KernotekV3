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
        stateC, statePython =  revisarProceso()
        if operation == "reporteTurno":
            startDate = request.form['fecha_inicio2'] + ' 00:00:00'
            endDate = request.form['fecha_fin2'] + ' 23:59:59'
            codeShifts = turnosDisponibles(startDate, endDate)
            if len(codeShifts) == 118:
                tablaFechas = False
            else:
                tablaFechas = True
            return render_template('reportesTurno.html', htmlTurnos=codeShifts, tablaFechas=tablaFechas)

        if operation == REPORT:
            typeReport = request.form['inpTipoReporte']
            # typeReport = typeReport[0]
            startDate = request.form['fecha_inicio'] + ' ' + request.form['hora_inicio']
            endDate = request.form['fecha_fin'] + ' ' + request.form['hora_fin']
            if typeReport == SHIFT_REPORT:
                startDate = request.form['fecha_inicio'] + ' 00:00:00'
                endDate = request.form['fecha_fin'] + ' 23:59:59'
                codeShifts = turnosDisponibles(startDate, endDate)
                if len(codeShifts) == 118:
                    tablaFechas = False
                else:
                    tablaFechas = True
                return render_template('reportesTurno.html', htmlTurnos=codeShifts, tablaFechas=tablaFechas, excel=False, PDF=False)

            if typeReport == DATES_REPORT:
                sells = class_db.reporte_general(startDate, endDate)
                tableHTML, codeOperations = tablaReporte(sells,startDate, endDate, "False", "False", "False")

                if len(tableHTML) == 66:
                    return render_template('reporteFechas.html', tableHTML=tableHTML, bandera=1, tablaFechas=False, reporte="General", acciones=codeOperations)
                else:
                    return render_template('reporteFechas.html', tableHTML=tableHTML, bandera=1, tablaFechas=True, reporte="General", acciones=codeOperations)

        if operation == CHANGE_RATE:
            #if stateC and statePython:
            newRate = request.form['nuevaTarifa']
	    print newRate
            class_db.cambiarTarifa(newRate)
            flag = "tarifaExitosa"
            #else:
            #    flag = "error"

        if operation == CHANGE_TIME_OPEN:
            if stateC and statePython:
                newTime = request.form['nuevoTiempo']
                class_db.cambiarTiempoApertura(newTime)
                flag = "tiempoExitoso"
            else:
                flag = "error"

        # if operation == CUT_SHIFT:
        #     if stateC and statePython:
        #         class_db.activarCorteTurno()
        #         time.sleep(2)  # Espera a que el corte de turno se ejecute
        #         flag = "corteExitoso"
        #     else:
        #         flag = "error"

        if operation == "cambiarManual":
            class_db.cambiarTipoCorte('0')
            flag = "cambioExitoso"
        
        if operation == "modalTurno":
            modalOperation = request.form['seleccionarAccion']
            # modalOperation = modalOperation[0]
            # if modalOperation == "cambiar":
            #     typeCut = request.form.getlist('tiposCorte')
            #     typeCut = typeCut[0]
            #     if typeCut == "manual":
            #         typeCut = '0'
            #     else:
            #         typeCut = '1'
            #         modalOperation = "configurar"
            #     class_db.cambiarTipoCorte(typeCut)
            #     flag = "cambioExitoso"
                # if stateC and statePython:
                #     class_db.cambiarTipoCorte(typeCut)
                #     flag = "cambioExitoso"
                # else:
                #     flag = "error"
                #     
            if modalOperation == '4':
                class_db.activarCorteTurno()
                time.sleep(2)   
                # if stateC and statePython:
                #     class_db.activarCorteTurno()
                #     time.sleep(2)  # Espera a que el corte de turno se ejecute
                #     flag = "corteExitoso"
                # else:
                #     flag = "error"

            if modalOperation == "3" or modalOperation == "1":
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
                # if typeLapse == 'cadaDetHora':
                #     timeAutoCut = request.form['hora']
                #     nextCut = libgral.generarProximoCorte(timeAutoCut)
                #     class_db.registroProxCorteAuto(nextCut)

                flag = "configuracionExitosa"
                class_db.cambiarTipoCorte('1')
                class_db.tipoTiempoAutomatico(typeLapse)
                class_db.tiempoCorteAuto(timeAutoCut)   

            

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
    diasmes = 0
    for dia in range(7):
	diapibote = diaActual - dia
	print dia
	if diapibote == 0:
		mes = mes -1
		diasmes = monthrange(year, mes)
		diasmes = diasmes[1]
		diaActual = diasmes
	print diaActual
	i = [diaActual - dia, 0]
	listaPibote.append(i)
    
    for dia in listaPibote:
	for x in datos:
	    if int(dia[0]) == int(x[0]):
		dia[1] = int(x[1])

    print listaPibote  
    for dia in listaPibote:
	d = datetime.datetime(year,mes, int(dia[0]))
	print d
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
                'acumuladoTurno': "",
                'ventasTurno': "",
                'etiqueta':" Hrs.",
                'ultimoTurno': str(class_db.ultimoTurno()),
                'cerradura': class_db.consultarCerradura()
                }

    if dic_home['ultimoTurno'] != "":
        dateShift = dic_home['ultimoTurno'].split(' ')
        date = dateShift[0].split('-')
        date = date[2] +'/'+ date[1]+'/'+ date[0]
        dateShift = date + " " +dateShift[1] + ' hrs.'
        dic_home['ultimoTurno'] = dateShift

    datosTurno = class_db.datosTurnoActual()
    numTurno = datosTurno[0]

    dic_home['acumuladoTurno'] = class_db.acumuladoTurno(str(numTurno))
    dic_home['ventasTurno'] = class_db.ventasTurno(str(numTurno))
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

    if dic_home['tipoCorte'] == 'automatico':
        banderaTiempo = class_db.consultarTipoTiempo()
        dic_home['tipoTiempo'] = banderaTiempo
        if banderaTiempo == "cadaDia":
            horaCorte = class_db.consultarTiempo()
            dic_home['automaticoHora'] = horaCorte
            dic_home['automaticoDia'] = ""
            dic_home['tipoTiempo'] = "Diario"
        if banderaTiempo == "cadaSemana":
            diaHora = class_db.consultarTiempo()
            diaHora = diaHora.split('|')
            dic_home['automaticoDia'] = diaHora[0]
            dic_home['automaticoHora']= diaHora[1] 
            dic_home['tipoTiempo'] = "Semanal"
        if banderaTiempo == "cadaMes":
            diaHora = class_db.consultarTiempo()
            diaHora = diaHora.split('|')
            dic_home['automaticoDia'] = diaHora[0]
            dic_home['automaticoHora']= diaHora[1]
            dic_home['tipoTiempo'] = "Mensual"
        dic_home['tipoCorte'] = "Automático"
    else:
        dic_home['tipoTiempo'] = ""
        dic_home['automaticoHora'] = ""
        dic_home['automaticoDia'] = ""
        dic_home['tipoCorte'] = "Manual"
        dic_home['etiqueta'] = ""
    return dic_home


