# -*- coding:utf-8 -*-
__author__ = 'aramirez'
import flask
from flask import render_template, redirect, session, request
import classdb
import excel


mensaje = str('<h1 class="text-center"><strong>No hay registros entre esas fechas</strong></h1>')

class reporteDetallado(flask.views.MethodView):
    def get(self):
        if len(session) > 1:
            return render_template('ReporteDetallado.html')
        else:
            return redirect('login')


    def post(self):
        linkDescarga = "../static/download/" + session['username'] + "/Reporte Detallado de Ventas.xlsx"
        fechaInicio = request.form['fecha_inicio'] + ' ' + request.form['hora_inicio']
        fechaFin = request.form['fecha_fin'] + ' ' + request.form['hora_fin']
        datosReporte = class_db.reportDetallado(fechaInicio, fechaFin)
        if len(datosReporte) == 0:
            return render_template('ReporteDetallado.html', mensaje=mensaje)
        else:
            excel.reporteDetallado(datosReporte, fechaInicio, fechaFin)
            return render_template('ReporteDetallado.html', bandera = 'archivoDescargar', linkDescarga = linkDescarga)
