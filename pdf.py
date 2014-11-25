# -*- coding:utf-8 -*-
# from xhtml2pdf import pisa
import class_db
import datetime
from flask import session
from weasyprint import HTML
import time


style="""
        @page{@top-left {content: url("file:/var/www/KernotekV3/static/img/PDF.png");}@bottom-right {content: "Página " counter(page) " de " counter(pages);font-size: .75em;padding-bottom: 6mm;}}
        img{border: 0;left: 50px;width: 180px;top: 20px;height: 60px;}
        .active{background-color: #f9f9f9;}
        .text-left {text-align: left;}
        .text-right {text-align: right;}
        .table > thead > tr .centrar{text-align:center;}
        .text-center {text-align: center;}
        .text-justify {text-align: justify;}
        table {background-color: transparent;}
        .table {width: 100%;max-width: 100%;margin-bottom: 20px;}
        h1 {margin: .67em 0;font-size: 2em;padding: 0;padding-bottom:0;}
        td{font: 100% sans-serif;text-align: center;padding: 1px;padding-top: 1px;}
        th{font: 100% sans-serif;background-color: #428BCA;color: white;padding-top: 1px;padding: 1px;text-align: center;}
        p{padding:0;padding-top:0;}
      """

def reporteEspecifico(datos, fechaInicio, fechaFin): 
    ruta = "/var/www/KernotekV3/static/download/"+session['username']+"/"
    fecha = str(datetime.datetime.today().strftime('%d-%b-%Y'))
    tiempo0 = time.time()
    codigoHTML = """
                    <html>
                    <head>
                    <style>
                    """+style+"""
                    </style>
                    </head>
                    <body>
                    <div class="text-right">"""+fecha+"""</div>
                    <div align="center">
                    <strong><h1 class="text-center">Resumen de ventas.</h1></strong>
                    <p class="text-center">de la fecha """+fechaInicio+"""  a la fecha """+fechaFin+"""</p>
                    </div>
                 """
    dicCabezeras = {'ticket': 'Ticket', 'localshift': 'Turno', 'datetimesell': 'Fecha', 'rate': 'Tarifa','deposit': 'Depósito'}
    cabezerasDisponibles = class_db.columnas_habilitadas()

    # Inicio de la tabla
    codigoHTML += """<table class="table">"""

    # Agregando las cabezera
    codigoHTML += """<thead>"""
    codigoHTML += """<tr>"""
    for cabezera in cabezerasDisponibles:
        codigoHTML += str("<th>")
        codigoHTML += dicCabezeras[cabezera]
        codigoHTML += str("</th>")
        
    codigoHTML += str("</tr>")
    codigoHTML += str("</thead>")

    # inicio del cuerpo de la tabla
    codigoHTML += str('<tbody class="text-center">')
    codigo = ""
    banderaFila = False

    for fila in datos:
        if banderaFila:
            codigo += ('<tr class="active">')
            banderaFila = False
        else:
            codigo += ('<tr>')
            banderaFila = True
        for dato in fila:
            if dato == 0:
                dato = "Cortesía"
            codigo += str('<td>') + str(dato) + str("</td>")

        codigo += ("</tr>")

    codigoHTML+= codigo
   
    # Etiquetas de cierre de la tabla
    codigoHTML += str("</tbody>")
    codigoHTML += str("</table>")

    # Etiquetas de cierre del html
    codigoHTML += str("</html>")
   
    HTML(string=codigoHTML).write_pdf(ruta + "Resumen de ventas.pdf")
    print time.time() - tiempo0 

def reporteGeneral(datos, fechaInicio, fechaFin):
    ruta = "/var/www/KernotekV3/static/download/"+session['username']+"/"
    fecha = str(datetime.datetime.today().strftime('%d-%b-%Y'))
    cabezeras = ['Tarifa', 'Número de Ventas', 'Total Acumulado']
    codigoHTML = """
                    <html>
                    <head>
                    <style>
                    """+style+"""
                    </style>
                    </head>
                    <body>
                    <div class="text-right">"""+fecha+"""</div>
                    <div align="center">
                    <strong><h1 class="text-center">Reporte general.</h1></strong>
                    <p class="text-center">De la fecha """+fechaInicio+"""  a la fecha """+fechaFin+""".</p>
                    </div>
                 """
    
    # Inicio de la tabla
    codigoHTML += """<table class="table">"""

    # Agregando las cabezera
    codigoHTML += """<thead>"""
    codigoHTML += """<tr>"""
    for cabezera in cabezeras:
        codigoHTML += str("<th>")
        codigoHTML += cabezera
        codigoHTML += str("</th>")
        
    codigoHTML += str("</tr>")
    codigoHTML += str("</thead>")

    # inicio del cuerpo de la tabla
    codigoHTML += str('<tbody class="text-center">')
    codigo = ""
    banderaFila = False

    for fila in datos:
        if banderaFila:
            codigo += ('<tr class="active">')
            banderaFila = False
        else:
            codigo += ('<tr>')
            banderaFila = True
        for dato in fila:
            if dato == 0:
                dato = "Cortesía"
            codigo += str('<td>') + str(dato) + str("</td>")

        codigo += ("</tr>")

    codigoHTML+= codigo
   
    # Etiquetas de cierre de la tabla
    codigoHTML += str("</tbody>")
    codigoHTML += str("</table>")

    # Calcula los totales de ventas y acumulado
    totales = class_db.totales(fechaInicio, fechaFin)  

    # Saltos de linea
    # codigoHTML += str('<font color="white">salto del linea</font><font color="white">salto de linea</font>')
    # codigoHTML += str('<font color="white">salto del linea</font><font color="white">salto de linea</font>')

    # Agredo de la tabla para los datos totales
    codigoHTML += """
                    <table class="table">
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

    # Etiquetas de cierre de la tabla de totales
    codigoHTML += str("</tbody>")
    codigoHTML += str("</table>")

    # Etiquetas de cierre del html
    codigoHTML += str("</html>")
    HTML(string=codigoHTML).write_pdf(ruta+'Reporte General.pdf')



def reporteTurno(datos, fechaInicio, fechaFin, numTurno):
    ruta = "/var/www/KernotekV3/static/download/"+session['username']+"/"
    fecha = str(datetime.datetime.today().strftime('%d-%b-%Y'))
    cabezeras = ['Ticket', 'Fecha', 'Tarifa', 'Multi.', 'Total', 'Depósito']

    codigoHTML = """
                    <html>
                    <head>
                    <style>
                    """+style+"""
                    </style>
                    </head>
                    <body>
                    <div class="text-right">"""+fecha+"""</div>
                    <div align="center">
                    <strong><h1 class="text-center">Reporte del turno """+str(numTurno)+""".</h1></strong>
                    <p class="text-center">De la fecha """+fechaInicio+"""  a la fecha """+fechaFin+""".</p>
                    </div>
                 """

    # Inicio de la tabla
    codigoHTML += """<table class="table">"""

    # Agregando las cabezera
    codigoHTML += """<thead>"""
    codigoHTML += """<tr>"""
    for cabezera in cabezeras:
        codigoHTML += str("<th>")
        codigoHTML += cabezera
        codigoHTML += str("</th>")

    # Etiquetas de cierre de la cabezera
    codigoHTML += str("</tr>")
    codigoHTML += str("</thead>")


    # inicio del cuerpo de la tabla
    codigoHTML += str('<tbody class="text-center">')
    codigo = ""
    count = 0
    banderaFila = False

    for fila in datos:
        if banderaFila:
            codigo += ('<tr class="active">')
            banderaFila = False
        else:
            codigo += ('<tr>')
            banderaFila = True
        count += 1
        for dato in fila:
            if dato == 0:
                dato = "Cortesía"
            codigo += str('<td>') + str(dato) + str("</td>")

        codigo += ("</tr>")
        if count == 1000:
            break

    codigoHTML+= codigo
   
    # Etiquetas de cierre de la tabla
    codigoHTML += str("</tbody>")
    codigoHTML += str("</table>")

    # Datos del total del turno
    montos = class_db.montosTurno(numTurno)

    # Saltos de linea 
    # codigoHTML += str('<font color="white">salto del linea</font><font color="white">salto de linea</font>')
    # codigoHTML += str('<font color="white">salto del linea</font><font color="white">salto de linea</font>')
    
    # Agreagdo de la tabla de totales del turno 
    codigoHTML += """
                    <table class="table">
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

    # Etiquetas de cierre de la tabla de totales del turno
    codigoHTML += str("</tbody>")
    codigoHTML += str("</table>")

    # Etiquetas de cierre del html
    codigoHTML += str("</html>")
    HTML(string=codigoHTML).write_pdf(ruta+'Reporte por turno.pdf')
