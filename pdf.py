# -*- coding:utf-8 -*-
from xhtml2pdf import pisa
import class_db
import datetime
from flask import session



def crearHTMLEspecifico(datos, fechaInicio, fechaFin):
    fechaReporte = str(datetime.datetime.today().strftime('%d-%b-%Y'))
    codigoHTML = """
<html>
    <head>
        <style>
             @page {
                size: a4 portrait;
                @frame header_frame {           /* Static Frame */
                    -pdf-frame-content: header_content;
                    -pdf-frame-content: header_content;
                    left: 50pt; width: 512pt; top: 50pt; height: 40pt;
                }
                @frame content_frame {          /* Content Frame */
                    left: 50pt; width: 512pt; top: 90pt; height: 632pt;
                }
                @frame footer_frame {           /* Another static Frame */
                    -pdf-frame-content: footer_content;
                    left: 50pt; width: 512pt; top: 772pt; height: 20pt;
                }
            }
            h1{
                font-family: "Tahoma";
            }
            table{
                    aling: center;
                    border: 1px solid gray;
                    text-align: center;
            }
            td{
                font: 100% sans-serif;
                align: center;
                text-align: center;
                padding: 1px;
                padding-top: 1px;

            }
            th{
                font: 100% sans-serif;
                align: center;
                background-color: #428BCA;
                color: white;
                padding-top: 1px;
                padding: 1px;
            }
        </style>
    </head>

    <body>
        <!-- Static Frame 'cabezera' -->
        <div id="header_content">
            <img src="reporte.jpg"/>
        </div>


        <!-- Static Frame 'pie de página' -->
        <div id="footer_content" align="right">p&aacute;gina  <pdf:pagenumber>
            de <pdf:pagecount>
        </div>

        <!-- Contenido HTML -->

        <div display="inline-block" id="content_frame">
            <strong><h2 align="right">FECHA: """+fechaReporte+"""</h2></strong>
        </div>
        <div align="center">
            <strong><h1>REPORTE DE VENTAS</h1></strong>
        </div>
        <div align="center">
            <strong><h1>De la fecha """+fechaInicio+""" a la fecha """+fechaFin+"""</h1></strong>
        </div>
"""
    dicCabezeras = {'ticket': 'Ticket', 'localshift': 'Turno', 'datetimesell': 'Fecha', 'rate': 'Tarifa',
                    'deposit': 'Deposito'}
    cabezerasDisponibles = class_db.columnas_habilitadas()
    banderaTabla = True  # Indica cuando inicia una tabla
    contador = 1  # Identifica cuantos registros estan en la tabla
    codigoTabla = ""
    banderaImagen = False  # Indica cuando poner la imagen de kernotek
    registrosPagina = 38  # Cuantos registros por pagina

    for fila in datos:
        contador += 1
        if banderaTabla:
            if banderaImagen:
                registrosPagina = 40
                codigoTabla += """
                                 <img src="reporte.jpg" height="50"/>
                               """
                banderaImagen = False

            codigoTabla += """
                             <table align="center">
                             <thead>
                          """
            codigoTabla += str('<tr>')
            for cabezera in cabezerasDisponibles:
                codigoTabla += str('<th>')
                codigoTabla += dicCabezeras[cabezera]
                codigoTabla += str('</th>')

            codigoTabla += str('</tr>')  # Fin de las cebezeras
            codigoTabla += str('</thead>')
            codigoTabla += str('<tbody class="text-center">')

            banderaTabla = False

        codigoTabla += str('<tr>')

        for dato in fila:
            if dato == 0:
                dato ="Token"
            codigoTabla += str("<td>") + str(dato) + str("</td>")

        codigoTabla += str("</tr>")

        if contador == registrosPagina:
            codigoTabla += str('</tbody>')   # Fin del contenido de la tabla
            codigoTabla += str('</table>')   # Fin de la tabla
            banderaTabla = True
            contador = 0
            banderaImagen = True

    codigoHTML += codigoTabla
    codigoHTML += """
                    </body>
                    </html>
                  """
    outputFilename = "static/download/"+session['username']+ "/Reporte de Ventas.pdf"
    pisa.showLogging()
    convertHtmlToPdf(codigoHTML, outputFilename)


def crearHTMLGeneral(datos, fechaInicio, fechaFin):
    outputFilename = "static/download/"+session['username']+"/Reporte General de Ventas.pdf"
    fechaReporte = str(datetime.datetime.today().strftime('%d-%b-%Y'))
    cabezeras = ['Tarifa', 'Número de Ventas', 'Total Acumulado']
    codigoHTML = """
<html>
    <head>
        <style>
             @page {
                size: a4 portrait;
                @frame header_frame {           /* Static Frame */
                    -pdf-frame-content: header_content;
                    left: 50pt; width: 512pt; top: 50pt; height: 40pt;
                }
                @frame content_frame {          /* Content Frame */
                    left: 50pt; width: 512pt; top: 90pt; height: 632pt;
                }
                @frame footer_frame {           /* Another static Frame */
                    -pdf-frame-content: footer_content;
                    left: 50pt; width: 512pt; top: 772pt; height: 20pt;
                }
            }
            h1{
                font-family: "Tahoma";
            }
            table{
                    aling: center;
                    border: 1px solid gray;
                    text-align: center;
            }
            td{
                font: 150% sans-serif;
                align: center;
                text-align: center;
                padding: 2px;
                padding-top: 3px;

            }
            th{
                font: 150% sans-serif;
                align: center;
                background-color: #428BCA;
                color: white;
                padding-top: 3px;
                padding: 2px;
            }
        </style>
    </head>

    <body>
        <!-- Static Frame 'cabezera' -->
        <div id="header_content">
            <img src="reporte.jpg"/>
        </div>


        <!-- Static Frame 'pie de página' -->
        <div id="footer_content" align="right">p&aacute;gina  <pdf:pagenumber>
            de <pdf:pagecount>
        </div>

        <!-- Contenido HTML -->

        <div display="inline-block" id="content_frame">
            <strong><h2 align="right">FECHA: """+fechaReporte+"""</h2></strong>
        </div>
        <div align="center">
            <strong><h1>REPORTE GENERAL DE VENTAS</h1></strong>
        </div>
        <div align="center">
            <strong><h1>De la fecha """+fechaInicio+""" a la fecha """+fechaFin+"""</h1></strong>
        </div>
"""
    banderaTabla = True  # Indica cuando inicia una tabla
    contador = 1  # Identifica cuantos registros estan en la tabla
    codigoTabla = ""
    banderaImagen = False  # Indica cuando poner la imagen de kernotek
    registrosPagina = 26  # Cuantos registros por pagina
    for fila in datos:
        contador += 1
        if banderaTabla:
            if banderaImagen:
                registrosPagina = 27
                codigoTabla += """
                                 <img src="reporte.jpg" height="50"/>
                               """
                banderaImagen = False

            codigoTabla += """
                             <table align="center">
                             <thead>
                          """
            codigoTabla += str('<tr>')
            for cabezera in cabezeras:
                codigoTabla += str('<th>')
                codigoTabla += cabezera
                codigoTabla += str('</th>')

            codigoTabla += str('</tr>')  # Fin de las cebezeras
            codigoTabla += str('</thead>')
            codigoTabla += str('<tbody class="text-center">')

            banderaTabla = False

        codigoTabla += str('<tr>')

        for dato in fila:
            codigoTabla += str("<td>") + str(dato) + str("</td>")

        codigoTabla += str("</tr>")

        if contador == registrosPagina:
            codigoTabla += str('</tbody>')   # Fin del contenido de la tabla
            codigoTabla += str('</table>')   # Fin de la tabla
            banderaTabla = True
            contador = 0
            banderaImagen = True

    codigoTabla += str('</tbody>')   # Fin del contenido de la tabla
    codigoTabla += str('</table>')   # Fin de la tabla

    totales = class_db.totales(fechaInicio, fechaFin)  #Calcula los totales de ventas y acumulado
    codigoTabla += str('<font color="white">salto del linea</font><font color="white">salto de linea</font>')
    codigoTabla += str('<font color="white">salto del linea</font><font color="white">salto de linea</font>')
    codigoTabla += """
                    <table>
                    <th colspan=2>TOTALES</th>
                    <tr>
                        <td color="white">Total de ventas</td>
                        <td>"""+str(totales[0][0])+"""</td>
                    </tr>
                    <tr>
                        <td color="white">Total Acumulado</td>
                        <td>$ """+str(totales[0][1])+"""</td>
                    </tr>
                    </table>
                    """
    codigoHTML += codigoTabla
    codigoHTML += """
                    </body>
                    </html>
                  """
    pisa.showLogging()
    convertHtmlToPdf(codigoHTML, outputFilename)



def crearHTMLReporteTurno(datos, fechaInicio, fechaFin, numTurno):
    outputFilename = "static/download/"+session['username']+"/Reporte por Turno.pdf"
    fechaReporte = str(datetime.datetime.today().strftime('%d-%b-%Y'))
    cabezeras = ['Ticket', 'Fecha', 'Tarifa', 'Mult', 'Total', 'Deposito']
    codigoHTML = """
<html>
    <head>
        <style>
             @page {
                size: a4 portrait;
                @frame header_frame {           /* Static Frame */
                    -pdf-frame-content: header_content;
                    -pdf-frame-content: header_content;
                    left: 50pt; width: 512pt; top: 50pt; height: 40pt;
                }
                @frame content_frame {          /* Content Frame */
                    left: 50pt; width: 512pt; top: 90pt; height: 632pt;
                }
                @frame footer_frame {           /* Another static Frame */
                    -pdf-frame-content: footer_content;
                    left: 50pt; width: 512pt; top: 772pt; height: 20pt;
                }
            }
            h1{
                font-family: "Tahoma";
            }
            table{
                    aling: center;
                    border: 1px solid gray;
                    text-align: center;
            }
            td{
                font: 100% sans-serif;
                align: center;
                text-align: center;
                padding: 1px;
                padding-top: 1px;

            }
            th{
                font: 100% sans-serif;
                align: center;
                background-color: #428BCA;
                color: white;
                padding-top: 1px;
                padding: 1px;
            }
        </style>
    </head>

    <body>
        <!-- Static Frame 'cabezera' -->
        <div id="header_content">
            <img src="reporte.jpg"/>
        </div>


        <!-- Static Frame 'pie de página' -->
        <div id="footer_content" align="right">p&aacute;gina  <pdf:pagenumber>
            de <pdf:pagecount>
        </div>

        <!-- Contenido HTML -->

        <div display="inline-block" id="content_frame">
            <strong><h2 align="right">FECHA: """+fechaReporte+"""</h2></strong>
        </div>
        <div align="center">
            <strong><h1>REPORTE DEL TURNO NÚMERO """+numTurno+"""</h1></strong>
        </div>
        <div align="center">
            <strong><h1>De la Fecha """+fechaInicio+""" a la Fecha """+fechaFin+"""</h1></strong>
        </div>
"""
    banderaTabla = True  # Indica cuando inicia una tabla
    contador = 1  # Identifica cuantos registros estan en la tabla
    codigoTabla = ""
    banderaImagen = False  # Indica cuando poner la imagen de kernotek
    registrosPagina = 38  # Cuantos registros por pagina
    for fila in datos:
        contador += 1
        if banderaTabla:
            if banderaImagen:
                registrosPagina = 40
                codigoTabla += """
                                 <img src="reporte.jpg" height="50"/>
                               """
                banderaImagen = False

            codigoTabla += """
                             <table align="">
                             <thead>
                          """
            codigoTabla += str('<tr>')
            for cabezera in cabezeras:
                codigoTabla += str('<th>')
                codigoTabla += cabezera
                codigoTabla += str('</th>')

            codigoTabla += str('</tr>')  # Fin de las cebezeras
            codigoTabla += str('</thead>')
            codigoTabla += str('<tbody class="text-center">')

            banderaTabla = False

        codigoTabla += str('<tr>')

        for dato in fila:
            codigoTabla += str("<td>") + str(dato) + str("</td>")

        codigoTabla += str("</tr>")

        if contador == registrosPagina:
            codigoTabla += str('</tbody>')   # Fin del contenido de la tabla
            codigoTabla += str('</table>')   # Fin de la tabla
            banderaTabla = True
            contador = 0
            banderaImagen = True

    codigoTabla += str('</tbody>')   # Fin del contenido de la tabla
    codigoTabla += str('</table>')   # Fin de la tabla

    montos = class_db.montosTurno(numTurno)
    codigoTabla += str('<font color="white">salto del linea</font><font color="white">salto de linea</font>')
    codigoTabla += str('<font color="white">salto del linea</font><font color="white">salto de linea</font>')
    codigoTabla += """
                    <table>
                    <th colspan=2>INFO. MONTO</th>
                    <tr>
                        <td color="white">Monto Inicial</td>
                        <td>$ """+str(montos[0][0])+"""</td>
                    </tr>
                    <tr>
                        <td color="white">Monto Final</td>
                        <td>$ """+str(montos[0][1])+"""</td>
                    </tr>
                    </table>
                    """
    codigoHTML += codigoTabla
    codigoHTML += """
                    </body>
                    </html>
                  """
    pisa.showLogging()
    convertHtmlToPdf(codigoHTML, outputFilename)



def convertHtmlToPdf(sourceHtml, outputFilename):
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
        sourceHtml,  # the HTML to convert
        dest=resultFile)  # file handle to recieve result

    # close output file
    resultFile.close()  # close output file
