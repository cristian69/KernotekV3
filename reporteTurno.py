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
            fecha = request.form['fecha_inicio']    
            htmlTurnos = turnosDisponibles(fecha)
            return render_template('reporteTurno.html', htmlTurnos=htmlTurnos)
      
        if bandera == "generarReporteTurno":
            numTurno = request.form['turnoSeleccionado']
            fechaInicioTurno = request.form['fechaInicial']
            fechaFinTurno = request.form['fechaFinal']
            registrosTurno = class_db.reporteTurno(numTurno)
            htmlTabla = tablaReporte(registrosTurno)
            
            excel.reporteTurno(registrosTurno, fechaInicioTurno, fechaFinTurno, numTurno)

            pdf.crearHTMLReporteTurno(registrosTurno, fechaInicioTurno, fechaFinTurno, numTurno)
            
            return render_template('reporteTurno.html', htmlTabla=htmlTabla)


    def get(self):
        if len(session) > 1:
            return render_template('reporteTurno.html')
        else:
            return redirect(url_for('login'))


def turnosDisponibles(fecha):
    turnos = class_db.turnosDisponibles(fecha)
    htmlTurnos = ""
    if len(turnos) == 0:
        htmlTurnos += '<h1 align="center"><strong>No Hay Cortes de Turnos en esa Fecha</strong></h1>'
    else:
        htmlTurnos += """
        <article class="portlet box green">
            <article class="portlet-title">
              <article class="caption">
                <i class="fa fa-bar-chart-o"></i>Turno Disponibles
              </article>
              <article class="tools">
                <a href="javascript:;" class="collapse"></a>
              </article>
            </article>
            <article class="portlet-body flip-scroll">
              <table class="table table-bordered table-striped table-condensed flip-content" id="tablaTurno">
                <thead class="flip-content text-center c-blue">
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

def tablaReporte(registros):
    cuerpoTabla = generar_tabla(registros, "", False)
    if not cuerpoTabla:
        codigoTabla = str('<h1></h1><h1 align="center"><strong>No hay registros de Ventas en ese Turno</strong></h1>')
        return codigoTabla
    linkExcel = "../static/download/"+session['username']+"/Reporte por Turno.xlsx"
    linkPDF = "../static/download/"+session['username']+"/Reporte por Turno.pdf"
    codigoTabla = """
                    <article class="portlet box green">
            <article class="portlet-title">
              <article class="caption">
                <i class="fa fa-bar-chart-o"></i>Reporte por Turno
              </article>
              <article class="tools">
                <a href=" """+linkExcel+""" " data-toggle="modal" class="blanc"><i class="fa fa-file-excel-o"></i></a>
                <a href=" """+linkPDF+""" " data-toggle="modal" class="blanc"><i class="fa fa-file-pdf-o"></i></a>
                <a href="javascript:;" class="collapse"></a>
              </article>
            </article>
            <article class="portlet-body flip-scroll">
              <table class="table table-bordered table-striped table-condensed flip-content">
                <thead class="flip-content text-center c-blue">
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
                       Deposito
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