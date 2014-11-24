# -*- coding: utf-8 -*-
__author__ = 'aramirez'

from flask import render_template, request, redirect, session, url_for
from class_db import reporte_general
from libgral import generar_tabla
import excel
import flask
import threading
import pdf


class reporteGeneral(flask.views.MethodView):
    def post(self):
        fechaInicio = request.form['fecha_inicio']
        horaInicio = request.form['hora_inicio']
        fechaFin = request.form['fecha_fin']
        horaFin = request.form['hora_fin']

        fechaInicio = fechaInicio + " " + horaInicio
        fechaFin = fechaFin + " " + horaFin
        datos = reporte_general(fechaInicio, fechaFin)
        reporte = tablaReporte(datos)
        #excel.reporteGeneral(datos, fechaInicio, fechaFin)
        PDF = threading.Thread(target=hiloPDF(datos, fechaInicio, fechaFin))
        PDF.start()

        return render_template('Reporte_General.html', reporte=reporte)

    def get(self):
        if len(session) > 1:
            return render_template('Reporte_General.html')
        else:
            return redirect(url_for('login'))


def hiloPDF(datos, fechaInicio, fechaFin):
    pdf.reporteGeneral(datos, fechaInicio, fechaFin)


def tablaReporte(datos, startDate, endDate):
    cuerpoTabla = generar_tabla(datos, "", False)
    if not cuerpoTabla:
        codigoTabla = str('<h1 align="center"><strong>No hay registros entre esas fechas</strong></h1>')
        return codigoTabla
    startDateReport = startDate.split(' ')
    date = startDateReport[0].split('-')
    startDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ startDateReport[1]
    endDateReport = endDate.split(' ')
    date = endDateReport[0].split('-')
    endDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ endDateReport[1]
    linkExcel = "../static/download/" + session['username'] + "/Reporte General.xlsx"
    linkDetallado = "../static/download/" +session['username']+ "/Reporte Detallado.xlsx"

    codeOperations = """
                    <article class="actions">
                        <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=especifico" class="btn btn-circle btn-default"> Especifico </a>
                        <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=detallado" class="btn btn-circle btn-default" id="detallado"> Generar Detallado </a>
                        <a href=" """+linkDetallado+""" " class="btn btn-circle blue-sunglo" id="descargarDetallado"><i class="fa fa-download"></i> Descargar Detallado </a>
                        <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=generarGeneral" class="btn btn-circle btn-default" id="generarExcel"><i class="fa fa-refresh"></i> Generar Excel </a>
                        <a href=" """+linkExcel+""" " class="btn btn-circle blue-sunglo" id="excelDescargar"><i class="fa fa-download"></i> Descargar Excel </a>
                    </article>
                     """
    codigoTabla = """
                    <article class="portlet light bordered">
            <article class="portlet-title">
              <article class="caption">
                <i class="fa fa-bar-chart-o"></i> De """+startDateReport+""" hrs. a """+endDateReport+""" hrs.
              </article>
            </article>
            <article class="portlet-body">
              <table class="table table-bordered table-condensed">
                <thead class="flip-content text-center">
                  <tr>
                    <th class="text-center">
                       Tarifa
                    </th>
                    <th class="text-center">
                       Número de Ventas
                    </th>
                    <th class="text-center">
                       Total
                    </th>
                  </tr>
                </thead>
                    """
    codigoTabla += str('<tbody class="text-center">') # Inicio del contenido de la tabla
    codigoTabla += cuerpoTabla # Cuerpo de la tabla

    #Etiquetas de cierre
    codigoTabla += """
                    </tbody>
                    </table>
                    </article>
                    </article>
                    """
    return codigoTabla, codeOperations
