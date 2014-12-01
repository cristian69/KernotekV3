# -*- coding: utf-8 -*-
__author__ = 'aramirez'
import flask
from flask import render_template, redirect, session, request, url_for
import class_db
from libgral import generar_tabla, numeracion_paginas
import excel
import pdf
from reporte_especifico import cod_tabla


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
            registrosTurno = class_db.reporteTurnoPaginacion(numTurno, 0)
            htmlTabla, codeOpertations = tablaReporte(registrosTurno, numTurno, fechaInicioTurno, fechaFinTurno, "False", "False")
            if len(htmlTabla) == 89:
                return render_template('reportesTurno.html', htmlTurnos=htmlTabla, tablaFechas=False, excel=False, PDF=False)
            # excel.reporteTurno(registrosTurno, fechaInicioTurno, fechaFinTurno, numTurno)
            # pdf.reporteTurno(registrosTurno, fechaInicioTurno, fechaFinTurno, numTurno)
            codepagination = paginacion(fechaInicioTurno, fechaFinTurno, 1, 0,
                                                       'reporte-turno', str(numTurno), "False", "False")
            return render_template('reportesTurno.html', htmlTurnos=htmlTabla, tablaFechas=True, excel=False, PDF=False, acciones=codeOpertations,
                                                        indexHtml=codepagination)


    def get(self):
        if len(session) > 1:
            index = str(request.args.get('indice'))
            date1 = request.args.get('fecha1')
            date2 = request.args.get('fecha2')

            actualpage = str(request.args.get('num_pagina'))
            typeReport = request.args.get('reporte')
            numShift = request.args.get('turno')
            startDate = request.args.get('fechaInicio')
            endDate = request.args.get('fechaFin')
            stateExcel = request.args.get('excel')
            statePDF = request.args.get('pdf')

            if index != 'None' and date1 != 'None' and date2 != 'None':
                codepagination = paginacion(date1, date2, actualpage, index,
                                                       'reporte-turno', numShift, stateExcel, statePDF)
                registrosTurno = class_db.reporteTurnoPaginacion(numShift, index)
                htmlTabla, codeOpertations = tablaReporte(registrosTurno, numShift, date1, date2, stateExcel, statePDF)
                return render_template('reportesTurno.html', htmlTurnos=htmlTabla,
                                       indexHtml=codepagination, tablaFechas= True, excel=stateExcel)


            if typeReport == "excel":
                sellShift = class_db.reporteTurno(numShift)
                salespagination = class_db.reporteTurnoPaginacion(numShift, 0)
                excel.reporteTurno(sellShift, startDate, endDate, numShift)
                tableHTML, codeOpertations = tablaReporte(salespagination, numShift, startDate, endDate, stateExcel="True", statePDF=statePDF)
                stateExcel = "True"
                
                if statePDF == "True":
                    statePDF = True
                else:
                    statePDF = False
                if stateExcel == "True":
                    stateExcel= True
                else:
                    stateExcel= False
                codepagination = paginacion(startDate, endDate, 1, 0,
                                                       'reporte-turno', str(numShift), stateExcel, statePDF)
                return render_template('reportesTurno.html', htmlTurnos=tableHTML, tablaFechas=True, excel=stateExcel, PDF= statePDF, acciones=codeOpertations,
                                                            indexHtml=codepagination)
            
            elif typeReport == "PDF":
                sellShift = class_db.reporteTurno(numShift)
                pdf.reporteTurno(sellShift, startDate, endDate, numShift)
                tableHTML, codeOpertations = tablaReporte(sellShift, numShift, startDate, endDate, stateExcel=stateExcel, statePDF="True")
                statePDF = "True"
                if statePDF == "True":
                    statePDF = True
                else:
                    statePDF = False
                if stateExcel == "True":
                    stateExcel= True
                else:
                    stateExcel= False
                
                return render_template('reportesTurno.html', htmlTurnos=tableHTML, tablaFechas=True, excel=stateExcel, PDF=statePDF, acciones=codeOpertations)
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
              <table class="table table-responsive table-condensed" id="tablaTurno">
                <thead class=" text-center">
                  <tr style="border-bottom:1px solid #E1E1E1;">
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

def tablaReporte(registros,  numTurno, fechaInicioTurno, fechaFinTurno, stateExcel, statePDF):
    cuerpoTabla = generar_tabla(registros, "", False)
    if not cuerpoTabla:
        codigoTabla = str('<h1></h1><h1 align="center"><strong>No hay registros de Ventas en ese Turno</strong></h1>')
        codeOpertations = ""
        return codigoTabla, codeOpertations 
    linkExcel = "../static/download/"+session['username']+"/Reporte por turno.xlsx"
    linkPDF = "../static/download/"+session['username']+"/Reporte por turno.pdf"
    codigoTabla = """
                    <article class="portlet light bordered">
            <article class="portlet-title">
              <article class="caption">
                <i class="fa fa-bar-chart-o"></i>Reporte por Turno
              </article>
              <article class="actions">
                <a href=" """+linkExcel+""" " class="btn blue-sunglo hidden" id="descargarTurnoExcel"> Descargar Excel </a>
                    <a href="/reporte-turno/?turno="""+numTurno+"""&fechaInicio="""+fechaInicioTurno+"""&fechaFin="""+fechaFinTurno+"""&reporte=excel&excel="""+stateExcel+"""&pdf="""+statePDF+""" "  class="btn btn-default" id="generarTurnoExcel">Generar Excel</a>
                    <a href="javascript:;" class="collapse"></a>
              </article>
            </article>
            <article class="portlet-body">
              <table class="table table-responsive table-condensed">
                <thead class="text-center ">
                  <tr style="border-bottom:1px solid #E1E1E1;">
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
    codeOpertations = """
                          <a href=" """+linkExcel+""" " class="btn blue-sunglo hidden" id="descargarTurnoExcel"> Descargar Excel </a>
                           <a href="/reporte-turno/?turno="""+numTurno+"""&fechaInicio="""+fechaInicioTurno+"""&fechaFin="""+fechaFinTurno+"""&reporte=excel&excel="""+stateExcel+"""&pdf="""+statePDF+""" "  class="btn btn-default" id="generarTurnoExcel">Generar Excel</a>
                          <a href="/reporte-turno/?turno="""+numTurno+"""&fechaInicio="""+fechaInicioTurno+"""&fechaFin="""+fechaFinTurno+"""&reporte=PDF&excel="""+stateExcel+"""&pdf="""+statePDF+""" "  class="btn btn-default" id="generarTurnoPdf">Generar PDF</a>
                          <a href=" """+linkPDF+""" " class="btn blue-sunglo hidden" id="descargarTurnoPdf"> Descargar PDF </a>
                          <a href="javascript:;" class="collapse"></a>
                      """
    return codigoTabla, codeOpertations




def paginacion(fecha_inicio, fecha_fin, pag_activa, indice, direccion, turno, stateexcel, statepdf):  # REGRESA EL CÓDIGO HTML DE LA PAGINACIÓN
    startDate = fecha_inicio
    endDate = fecha_fin
    actualPage = int(pag_activa)
    startRange = int(indice)
    link = direccion
    codeIndex = ""
    codeIndex = str('<article class="text-right dataTables_paginate paging_bootstrap_full_number">')
    codeIndex += str('<ul class="pagination">')

    # Simbolo <<
    if actualPage == 1:
        codeIndex += str('<li class="disabled prev"><a href="#"><i class="fa fa-angle-double-left"></i></a></li>')
        
    else:
        pagePreviousBlock = actualPage - 10
        if pagePreviousBlock <= 0:
            pagePreviousBlock = 1

        rangePreviousBlock = startRange - 500
        if rangePreviousBlock <= 0:
            rangePreviousBlock = 0

        codeIndex += str('<li class="enable prev"> <a href="/'+link+'/?' \
            'indice=' + str(rangePreviousBlock) +\
            '&fecha1=' + startDate + \
            '&fecha2='  + endDate + \
            '&turno=' + str(turno) + \
            '&excel=' +str(stateexcel)+\
            '&pdf=' +str(statepdf)+\
            '&num_pagina=' + str(pagePreviousBlock) + '">'\
            '<i class="fa fa-angle-double-left"></i></a></li>') 

    # Simbolo <
    if actualPage == 1:
        codeIndex += str('<li class="disabled prev"><a href="#"><i class="fa fa-angle-left"></i></a></li>')
    else:
        previousPage = actualPage - 1
        rengePreviousPage = startRange - 50
        codeIndex += str('<li class="enable prev"><a href="/'+link+'/?'\
            'indice='+ str(rengePreviousPage) + \
            '&fecha1='+ startDate + \
            '&fecha2='+ endDate + \
            '&turno=' + str(turno) + \
            '&excel=' +str(stateexcel)+\
            '&pdf=' +str(statepdf)+\
            '&num_pagina='+ str(previousPage) +'">'\
            '<i class="fa fa-angle-left"></i></a></li>')

    sales = int(class_db.total_registros(startDate, endDate, startRange))
    restSales = sales
    countPage = 0
    startPage = actualPage
    rangePage = startRange
    for x in range(sales):
        countPage += 1
        if countPage == 50:
            if startPage is actualPage:
                codeIndex += str('<li class="active" id="pag'+str(startPage)+'">')
            else:
                codeIndex += str('<li id="pag'+str(startPage)+'">')

            codeIndex += str('<a href="/'+link+'/?'\
                    'indice='+ str(rangePage) + \
                    '&fecha1='+ startDate + \
                    '&fecha2='+ endDate + \
                    '&turno=' + str(turno) + \
                    '&excel=' +str(stateexcel)+\
                    '&pdf=' +str(statepdf)+\
                    '&num_pagina='+ str(startPage) + '">'\
                    +str(startPage)+
                    '</a></li>')

            startPage += 1
            rangePage += 50
            countPage = 0
            restSales -= 50
    if restSales > 0:
        if startPage is actualPage:
            codeIndex += str('<li class="active" id="pag'+str(startPage)+'">')
        else:
            codeIndex += str('<li id="pag'+str(startPage)+'">')
        codeIndex += str('<a href="/'+link+'/?'\
                    'indice='+ str(rangePage) + \
                    '&fecha1='+ startDate + \
                    '&fecha2='+ endDate + \
                    '&turno=' + str(turno) + \
                    '&excel=' +str(stateexcel)+\
                    '&pdf=' +str(statepdf)+\
                    '&num_pagina='+ str(startPage) + '">'\
                    +str(startPage)+
                    '</a></li>')

    # Simbolo >
    nextPage = actualPage + 1
    rangeNextPage = startRange + 50

    salesNextPage = class_db.total_registros(startDate, endDate, startRange + 50)

    if salesNextPage == 0:
        codeIndex += str('<li class="disabled"><a href="#"><i class="fa fa-angle-right"></i></a></li>')
    else:
        codeIndex += str('<li class="enable"><a href="/'+link+'/?'\
                    'indice='+str(rangeNextPage)+\
                    '&fecha1=' + startDate +\
                    '&fecha2=' + endDate +\
                    '&turno=' + str(turno) + \
                    '&excel=' +str(stateexcel)+\
                    '&pdf=' +str(statepdf)+\
                    '&num_pagina=' + str(nextPage) + '">'
                    '<i class="fa fa-angle-right"></i></a></li>')
    
    # Simbolo >>
    salesNextBlock = class_db.total_registros(startDate, endDate, startRange + 500)
    nextBlock = actualPage + 10
    rangeNextBlock = startRange + 500
    if salesNextBlock == 0:
        codeIndex += str('<li class="disabled"><a href="#"><i class="fa fa-angle-double-right"></i></a></li>')
    else:
        codeIndex += str('<li class="enable"><a href="/'+link+'/?'\
                    'indice='+ str(rangeNextBlock)+\
                    '&fecha1=' + startDate +\
                    '&fecha2=' + endDate +\
                    '&turno=' + str(turno) + \
                    '&excel=' +str(stateexcel)+\
                    '&pdf=' +str(statepdf)+\
                    '&num_pagina=' + str(nextBlock) +'">'\
                    '<i class="fa fa-angle-double-right"></i></a></li>')
    return codeIndex
