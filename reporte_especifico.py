# -*- coding: utf-8 -*-
__author__ = 'aramirez'
import flask
from flask import render_template, redirect, session, request, url_for
from libgral import numeracion_paginas
import class_db
import excel
import threading
import pdf
from datetime import datetime

banderaPDF = True
try:
    import pdf
except:
    print "Falta de instalar la libreria xhtml2pdf de python"
    banderaPDF = False


class reporteEspecifico(flask.views.MethodView):
    def post(self):
        fecha1 = request.form['fecha_inicio']
        hora1 = request.form['hora_inicio']
        fecha2 = request.form['fecha_fin']
        hora2 = request.form['hora_fin']
        fecha_inicio = fecha1 + " " + hora1
        fecha_fin = fecha2 + " " + hora2
        codigo_paginacion = numeracion_paginas(fecha_inicio, fecha_fin, 1, 0, 'reporte-especifico')
        codigo_tabla = cod_tabla(fecha_inicio, fecha_fin, 0)
        if len(codigo_tabla) == 66:
            return render_template('Reporte_Especifico.html', codigo_tabla=codigo_tabla)
        else:
            datos_reporte = class_db.reporte_especifico(fecha_inicio, fecha_fin)
            #thread_excel = threading.Thread(target=hilo_excel(datos_reporte, fecha_inicio, fecha_fin), name="hilo Excel")
            #thread_excel.start()
            pdf.reporteEspecifico(datos_reporte, fecha_inicio, fecha_fin)
            #if banderaPDF:
        #pass
                #thread_pdf = threading.Thread(target=hiloPDF(datos_reporte, fecha_inicio, fecha_fin), name="hilo PDF")
                #thread_pdf.start()

            return render_template('Reporte_Especifico.html', codigo_paginacion=codigo_paginacion,
                                   codigo_tabla=codigo_tabla)

    def get(self):
        if len(session) > 1:
            indice = str(request.args.get('indice'))
            fecha_inicio = str(request.args.get('fecha1'))
            fecha_fin = str(request.args.get('fecha2'))
            pagina_activa = str(request.args.get('num_pagina'))
            if indice != 'None' and fecha_inicio != 'None' and fecha_fin != 'None':
                codigo_paginacion = numeracion_paginas(fecha_inicio, fecha_fin, pagina_activa, indice,
                                                       'reporte-especifico')
                codigo_tabla = cod_tabla(fecha_inicio, fecha_fin, indice)
                return render_template('Reporte_Especifico.html', codigo_paginacion=codigo_paginacion,
                                       codigo_tabla=codigo_tabla)
            else:
                return render_template('Reporte_Especifico.html')
        else:
            return redirect(url_for('login'))


def cod_tabla(startDate, endDate, inicio):
    startDateReport = startDate.split(' ')
    date = startDateReport[0].split('-')
    startDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ startDateReport[1]
    endDateReport = endDate.split(' ')
    date = endDateReport[0].split('-')
    endDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ endDateReport[1]

    linkExcel = "../static/download/"+ session['username'] + "/Reporte de Ventas.xlsx"
    linkDetallado = "../static/download/" +session['username']+ "/Reporte Detallado.xlsx"
    # linkPDF = "../static/download/"+ session['username'] + "/Reporte de Ventas.pdf"
    dicCabezeras = {'ticket': 'Ticket', 'localshift': 'Turno', 'datetimesell': 'Fecha', 'rate': 'Tarifa',
                    'deposit': 'Depósito'}
    cabezerasDisponibles = class_db.columnas_habilitadas()
    codigo_tabla = ""
    bandera_color = True
    codigo_tabla += str('<div class="portlet light bordered">')  # Código del div
    codigo_tabla += str(""" <div class="portlet-title">
            <div class="caption">
              <i class="fa fa-bar-chart-o text-center"></i>De""" + startDateReport + """ hrs. a """ + endDateReport + """ hrs.
            </div>
          </div>
          <div class="portlet-body" >
            <table class="table table-responsive  table-condensed ">""")

    codigo_tabla += str('<thead class="text-center ">')  # Etiqueta de head para la tabla
    codigo_tabla += str('<tr  style="border-bottom:1px solid #E1E1E1;"">')  # Inicio de las cabezeras
    dicVenta = []
    for cabezera in cabezerasDisponibles:
        codigo_tabla += str('<th width="20%"class="text-center">')
        codigo_tabla += dicCabezeras[cabezera]
        dicVenta.append( dicCabezeras[cabezera] )
        codigo_tabla += str('</th>')

    codigo_tabla += str('</tr>')  # Fin de las cebezeras
    codigo_tabla += str('</thead>')  # Fin de head

    codigo_tabla += str('<tbody class="text-center">')  # Inicio del contenido de la tabla
    tabla_ventas = class_db.paginacion(startDate, endDate, inicio)

    if len(tabla_ventas) == 0:
        return str('<h1 align="center"><strong>No hay registro de ventas</strong></h1>')
    else:

        codeOperations = """
                            <div class="actions">
                                <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=general"  class="btn btn-circle btn-default"> General </a>
                                <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=detallado"  id="detallado"class="btn btn-circle btn-default"> Generar Detallado </a>
                                <a href=" """+linkDetallado+""" " class="btn btn-circle blue-sunglo hidden" id="descargarDetallado"><i class="fa fa-download"></i> Descargar Detallado </a>
                                <a href=" /reportes/?fecha1="""+startDate+"""&fecha2="""+endDate+"""&reporte=generarEspecifico"  class="btn btn-circle btn-default" id="generarExcel"> Generar Excel </a>
                                <a href=" """+linkExcel+""" " class="btn btn-circle blue-sunglo hidden" id="excelDescargar"><i class="fa fa-download"></i> Descargar Excel </a>
                            </div>
                         """
        for ventas in tabla_ventas:
            if bandera_color:
                codigo_tabla += str('<tr  style="border-bottom:1px solid #E1E1E1;">')
                bandera_color = False
            else:
                codigo_tabla += str('<tr style="border-bottom:1px solid #E1E1E1;">')
                bandera_color = True
            for venta, columna in zip(ventas, dicVenta):
                if columna == "Depósito"and venta == 0:
                    venta = "Cortesía"
                codigo_tabla += str("<td>") + str(venta) + str("</td>")
            codigo_tabla += str("</tr>")

    codigo_tabla += str('</tbody>')  #Fin del contenido de la tabla
    codigo_tabla += str('</table></div></div>')  # Fin de la tabla
    return codigo_tabla, codeOperations


def hilo_excel(ventas, fecha_inicio, fecha_fin):
    obj_excel = excel
    obj_excel.export_excel(ventas, fecha_inicio, fecha_fin)


def hiloPDF(datos_reporte, fecha_inicio, fecha_fin):
    pdf.crearHTMLEspecifico(datos_reporte, fecha_inicio, fecha_fin)
