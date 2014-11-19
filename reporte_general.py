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
    linkExcel = "../static/download/"+session['username']+"/Reporte General de Ventas.xlsx"
    linkPDF = "../static/download/"+session['username']+"/Reporte General de Ventas.pdf"
    # linkExcel = "/var/www/demoFlask/static/download/" + session['username'] + "/Reporte General de Ventas.xlsx"
    codigoTabla = """
                    <article class="portlet light bordered">
            <article class="portlet-title">
              <article class="caption">
                <i class="fa fa-bar-chart-o"></i>Reporte General
              </article>
              <article class="actions">
                <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=especifico" class="btn btn-circle btn-default"> Especifico </a>
                <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=detallado" class="btn btn-circle btn-default"> Detallado </a>
                <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=generarGeneral" class="btn btn-circle btn-default" id="generarExcel"><i class="fa fa-refresh"></i> Generar Excel </a>
                <a href=" """+linkExcel+""" " class="btn btn-circle blue-sunglo" id="excelDescargar"><i class="fa fa-download"></i> Descargar Excel </a>
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
    return codigoTabla
