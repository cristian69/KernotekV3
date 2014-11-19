# -*- coding: utf-8 -*-
__author__ = 'aramirez'
import flask
from flask import render_template, redirect, session, request, url_for
import class_db
from libgral import generar_tabla
import excel
import pdf

class reporteTurno(flask.views.MethodView):
    def post(self):
        bandera = request.form['submit']
        if bandera == "buscarTurnos":   
            startDate = request.form['fecha_inicio'] + " 00:00:00"
            endDate = request.form['fecha_fin'] + " 23:59:59"
            htmlTurnos = turnosDisponibles(startDate, endDate)
            if len(htmlTurnos) == 118:
                tablaFechas = False
            else:
                tablaFechas = True
            return render_template('reportesTurno.html', htmlTurnos=htmlTurnos, tablaFechas=tablaFechas)
      
        if bandera == "generarReporteTurno":
            numTurno = request.form['turnoSeleccionado']
            fechaInicioTurno = request.form['fechaInicial']
            fechaFinTurno = request.form['fechaFinal']
            registrosTurno = class_db.reporteTurno(numTurno)
            htmlTabla = tablaReporte(registrosTurno, numTurno, fechaInicioTurno, fechaFinTurno)
            if len(htmlTabla) == 89:
                return render_template('reportesTurno.html', htmlTurnos=htmlTabla, tablaFechas=False, excel=False, PDF=False)
            # excel.reporteTurno(registrosTurno, fechaInicioTurno, fechaFinTurno, numTurno)
            # pdf.reporteTurno(registrosTurno, fechaInicioTurno, fechaFinTurno, numTurno)
            return render_template('reportesTurno.html', htmlTurnos=htmlTabla, tablaFechas=True, excel=False, PDF=False)


    def get(self):
        if len(session) > 1:
            typeReport = request.args.get('reporte')
            numShift = request.args.get('turno')
            startDate = request.args.get('fechaInicio')
            endDate = request.args.get('fechaFin')
            if typeReport == "excel":
                sellShift = class_db.reporteTurno(numShift)
                excel.reporteTurno(sellShift, startDate, endDate, numShift)
                tableHTML = tablaReporte(sellShift, numShift, startDate, endDate)
                return render_template('reportesTurno.html', htmlTurnos=tableHTML, tablaFechas=True, excel=True, PDF= False)
            elif typeReport == "PDF":
                sellShift = class_db.reporteTurno(numShift)
                pdf.reporteTurno(sellShift, startDate, endDate, numShift)
                tableHTML = tablaReporte(sellShift, numShift, startDate, endDate)
                return render_template('reportesTurno.html', htmlTurnos=tableHTML, tablaFechas=True, excel=False, PDF=True)
            else:
                return render_template('reportesTurno.html', htmlTurnos="", tablaFechas=False, excel=False, PDF=False)
        else:
            return redirect(url_for('login'))


def turnosDisponibles(startDate, endDate):
    turnos = class_db.turnosDisponibles(startDate, endDate)
    htmlTurnos = ""
    if len(turnos) == 0:
        htmlTurnos += '<h1  style="line-height:1.1 !important;" align="center"><strong>No se encontraron turnos en esas fechas.</strong></h1>'
    else:
        htmlTurnos += """
        <article class="portlet light bordered">
            <article class="portlet-title">
              <article class="caption">
                <i class="fa fa-bar-chart-o"></i>Turno Disponibles
              </article>

            </article>
            <article class="portlet-body ">
              <table class="table table-bordered table-condensed" id="tablaTurno">
                <thead class=" text-center">
                  <tr>
                    <th class="text-center">
                       Número de Corte
                    </th>
                    <th class="text-center">
                       Fecha Inicial
                    </th>
                    <th class="text-center">
                       Fecha Final
                    </th>
                  </tr>
                </thead>
                    """
        cuerpoTabla = str('<tbody class="text-center">') # Inicio del contenido de la tabla
        cuerpoTabla += generar_tabla(turnos, "tablaTurno", False)
        htmlTurnos += cuerpoTabla
        htmlTurnos += """
                    </tbody>
                    </table>
                    </article>
                    </article>
                    """
    return htmlTurnos

def tablaReporte(registros,  numTurno, fechaInicioTurno, fechaFinTurno):
    cuerpoTabla = generar_tabla(registros, "", False)
    if not cuerpoTabla:
        codigoTabla = str('<h1></h1><h1 align="center"><strong>No hay registros de Ventas en ese Turno</strong></h1>')
        return codigoTabla
    linkExcel = "../static/download/"+session['username']+"/Reporte por Turno.xlsx"
    linkPDF = "../static/download/"+session['username']+"/Reporte por Turno.pdf"
    codigoTabla = """
                    <article class="portlet light bordered">
            <article class="portlet-title">
              <article class="caption">
                <i class="fa fa-bar-chart-o"></i>Reporte por Turno
              </article>
              <article class="actions">
                <a href=" """+linkExcel+""" " class="btn btn-circle btn-default hidden" id="descargarTurnoExcel">Descargar Excel</a>
                <a href="/reporte-turno/?turno="""+numTurno+"""&fechaInicio="""+fechaInicioTurno+"""&fechaFin="""+fechaFinTurno+"""&reporte=excel "  class="btn btn-circle btn-default" id="generarTurnoExcel">Generar Excel</a>
                <a href="/reporte-turno/?turno="""+numTurno+"""&fechaInicio="""+fechaInicioTurno+"""&fechaFin="""+fechaFinTurno+"""&reporte=PDF "  class="btn btn-circle btn-default" id="generarTurnoPdf">Generar PDF</a>
                <a href=" """+linkPDF+""" " class="btn btn-circle btn-default hidden" id="descargarTurnoPdf">Descargar PDF</a>
                <a href="javascript:;" class="collapse"></a>
              </article>
            </article>
            <article class="portlet-body">
              <table class="table table-bordered table-condensed">
                <thead class="text-center ">
                  <tr>
                    <th class="text-center">
                       Ticket
                    </th>
                    <th class="text-center">
                       Fecha
                    </th>
                    <th class="text-center">
                       Tarifa
                    </th>
                    <th class="text-center">
                       Multiplicador
                    </th>
                    <th class="text-center">
                       Total
                    </th>
                    <th class="text-center">
                       Depósito
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
