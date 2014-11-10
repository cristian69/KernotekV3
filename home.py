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

class Home(flask.views.MethodView):
    def get(self):
        if len(session) > 1:
            dic_home = datos_home()
            #print dic_home
            return render_template('home.html',dic_home=dic_home)
        else:
            ip = request.remote_addr
            logger.seguridad('INTENTO DE BURLAR LA SEGURIDAD| IP RESPONSABLE: ' + ip)
            return redirect(url_for('login'))



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
        for mes in datos:
            m = datetime.datetime(2014,mesActual,1)
            if int(mes[0]) == mesActual:
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
        for semana in datos:
            if int(semana[0]) == semanaActual:
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

    fecha = str(ObtenerFecha()).split('-')
    year = int(fecha[0])
    mes = int(fecha[1])
    ultimoDia = monthrange(year,mes)
    ultimoDia = int(ultimoDia[1])
    
    diaActual = int(obtenerDia())
    listaDias = []
    listaVentas = []
    for i in range(0,7):
        for dia in datos:
            if int(dia[0]) == diaActual:
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


