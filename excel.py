# -*- coding: utf-8 -*-
from itertools import count

__author__ = 'aramirez'
import class_db
import xlsxwriter
import datetime
from flask import session


def export_excel(data, date_start, date_end):
    startDateReport = date_start.split(' ')
    date = startDateReport[0].split('-')
    startDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ startDateReport[1]
    endDateReport = date_end.split(' ')
    date = endDateReport[0].split('-')
    endDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ endDateReport[1]

    dateReport = datetime.date.today()
    dateReport = str(dateReport).split('-')
    dateReport = dateReport[2] +'/'+ dateReport[1] +'/'+ dateReport[0] 

    total_sells = data
    total_registros = 10  # Indica donde comenzar

   
    columns = class_db.columnas_habilitadas()

    rute_and_name = "/var/www/kernotekv3/static/download/" + session['username'] + "/Reporte Específico.xlsx"

    book = xlsxwriter.Workbook(rute_and_name)

    sheet = book.add_worksheet()

    sheet.name = "Ventas"


    # FORMATOS DE LOS DATOS
    # color , 'bg_color': '#428BCA'
    string_format = book.add_format({'bold': True,
                                     'font_size': 10,
                                     'font_name': 'Arial',
                                     'align': 'center',
                                     'valign': 'vcenter'})

    num_format = book.add_format({'align': 'center',
                                  'border': 1,
                                  'font_name': 'Arial'})

    dateTime_format = book.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss',
                                       'align': 'center',
                                       'border': 1,
                                       'font_name': 'Arial'})

    cash_foramt = book.add_format({'num_format': '[$$-80A]#,##0.00;[RED]-[$$-80A]#,##0.00',
                                   'align': 'center',
                                   'border': 1,
                                   'font_name': 'Arial'})

    header_format = book.add_format({'align': 'center',
                                     'border': 1,
                                     'bold': True,
                                     'font_color': '#FFFFFF',
                                     'bg_color': '#428BCA',
                                     'font_name': 'Arial'})


    # INSERTAR IMAGEN CON ESCALA
    sheet.insert_image('A1', 'static/img/reporte.png', {'x_scale': 0.5, 'y_scale': 0.5})

    # DATOS DE LA HOJA
    sheet.merge_range('A4:C4', 'ICT Consulting', string_format)
    sheet.merge_range('E4:F4', 'Fecha: ' + str(dateReport), string_format)
    sheet.merge_range('B6:F6', 'Reporte especifico', string_format)
    sheet.merge_range('B8:F8', 'Del ' + startDateReport + ' hrs. AL ' + endDateReport + ' hrs.', string_format)


    # DATOS DE LA TABLA
    data = []
    for sells in total_sells:
        data2 = []
        for sell in sells:
            if sell == 0:
                sell = "Cortesía"
            data2.append(sell)
        data.append(data2)

    # FORMATO DE LA TABLA

    # --------<CABEZERAS DINAMICAS>---------------------
    col = ('B', 'C', 'D', 'E', 'F')
    row = 10
    count = 0

    cells_format = {'ticket': {'format': num_format},  # Diccionario con los diferentes tipos de formatos
                    'localshift': {'format': num_format},
                    'datetimesell': {'format': dateTime_format},
                    'no_detalle': {'format': num_format},
                    'rate': {'format': cash_foramt},
                    'deposit': {'format': cash_foramt}}

    nom_colum = {'ticket': 'Ticket',
                 'localshift': 'Turno',
                 'datetimesell': 'Fecha',
                 'no_detalle': 'Número de Detalle',
                 'rate': 'Tarifa',
                 'deposit': 'Deposito'}

    headers = []
    format_columns = []

    for column in columns:  # Cambia el nombre de las columna
        headers.append(nom_colum[column])
        format_columns.append(cells_format[column])

    for column in headers:
        sheet.write(col[count] + str(row), column, header_format)  # Inserta las columnas que estan disponibles
        if column == 'Fecha':
            sheet.set_column(col[count] + ':' + col[count], 20)  # TAMAÑO DE LA CELDA FECHA
        count += 1

    sheet.set_column('D:D', 20)  # TAMAÑO DE LA CELDA

    format_columns.append({'format': num_format})
    format_columns.append({'format': num_format})
    format_columns.append({'format': num_format})
    format_columns.append({'format': num_format})

    total_registros += len(data)  # indica el fin da la tabla

    #-------<DATOS DE LAS CELADAS>-----------
    tam_table = 'B10:F' + str(total_registros)
    sheet.add_table(tam_table, {'name': 'Reporte de ventas del dia',
                                'banded_columns': True,
                                'header_row': False,
                                'data': data,
                                'autofilter': False,
                                'columns': format_columns})

    book.close()


def reporteGeneral(data, date_start, date_end):
    startDateReport = date_start.split(' ')
    date = startDateReport[0].split('-')
    startDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ startDateReport[1]
    endDateReport = date_end.split(' ')
    date = endDateReport[0].split('-')
    endDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ endDateReport[1]

    dateReport = datetime.date.today()
    dateReport = str(dateReport).split('-')
    dateReport = dateReport[2] +'/'+ dateReport[1] +'/'+ dateReport[0] 

    total_sells = data
    total_registros = 10
   

    columns = ['Tarifa', 'Número de Ventas', 'Total Acumulado']

    rute_and_name = "/var/www/kernotekv3/static/download/" + session['username'] + "/Reporte General.xlsx"

    book = xlsxwriter.Workbook(rute_and_name)

    sheet = book.add_worksheet()

    sheet.name = "Ventas"


    # FORMATOS DE LOS DATOS
    # color , 'bg_color': '#428BCA'
    string_format = book.add_format({'bold': True,
                                     'font_size': 10,
                                     'font_name': 'Arial',
                                     'align': 'center',
                                     'valign': 'vcenter'})

    num_format = book.add_format({'align': 'center',
                                  'border': 1,
                                  'font_name': 'Arial'})

    cash_foramt = book.add_format({'num_format': '[$$-80A]#,##0.00;[RED]-[$$-80A]#,##0.00',
                                   'align': 'center',
                                   'border': 1,
                                   'font_name': 'Arial'})

    header_format = book.add_format({'align': 'center',
                                     'border': 1,
                                     'bold': True,
                                     'font_color': '#FFFFFF',
                                     'bg_color': '#428BCA',
                                     'font_name': 'Arial'})


    # INSERTAR IMAGEN CON ESCALA
    sheet.insert_image('A1', 'static/img/reporte.png', {'x_scale': 0.5, 'y_scale': 0.5})

    # DATOS DE LA HOJA
    sheet.merge_range('A4:C4', 'SERVICIO SECA S.A DE C.V', string_format)
    sheet.merge_range('E4:F4', 'Fecha: ' + str(dateReport), string_format)
    sheet.merge_range('B6:F6', 'REPORTE GENERAL.', string_format)
    sheet.merge_range('B8:F8', 'Del ' + startDateReport + ' hrs. AL ' + endDateReport + ' hrs.', string_format)


    # DATOS DE LA TABLA
    data = []

    for sells in total_sells:
        data2 = []
        for sell in sells:
            data2.append(sell)
        data.append(data2)

    # FORMATO DE LA TABLA

    # --------<CABEZERAS DINAMICAS>---------------------
    col = ('C', 'D', 'E')
    row = 10
    count = 0

    format_columns = []

    for column in columns:
        sheet.write(col[count] + str(row), column, header_format)  # Inserta las columnas que estan disponibles
        count += 1

    sheet.set_column('C:C', 20)
    sheet.set_column('D:D', 20)  # TAMAÑO DE LA CELDA
    sheet.set_column('E:E', 20)

    #-------<DATOS DE LAS CELADAS>-----------

    format_columns.append({'format': cash_foramt})
    format_columns.append({'format': num_format})
    format_columns.append({'format': cash_foramt})

    total_registros += len(data)
    tam_table = 'C10:E' + str(total_registros)
    sheet.add_table(tam_table, {'name': 'Reporte de ventas',
                                'banded_columns': True,
                                'header_row': False,
                                'data': data,
                                'columns': format_columns})

    totales = class_db.totales(date_start, date_end)

    sheet.merge_range('C' + str(len(data) + 12) + ':D' + str(len(data) + 12), 'TOTAL', header_format)
    sheet.write('C' + str(len(data) + 13), 'Total de Ventas', header_format)
    sheet.write('C' + str(len(data) + 14), 'Total Acumulado', header_format)

    sheet.write('D' + str(len(data) + 13), totales[0][0], num_format)
    sheet.write('D' + str(len(data) + 14), totales[0][1], cash_foramt)
    book.close()


def reporteDetallado(data, date_start, date_end):
    total_sells = data

    startDateReport = date_start.split(' ')
    date = startDateReport[0].split('-')
    startDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ startDateReport[1]
    endDateReport = date_end.split(' ')
    date = endDateReport[0].split('-')
    endDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ endDateReport[1]
    total_registros = 10  # Indica donde comenzar

    dateReport = datetime.date.today()
    dateReport = str(dateReport).split('-')
    dateReport = dateReport[2] +'/'+ dateReport[1] +'/'+ dateReport[0] 
    columns = ['Ticket', 'Turno', 'Fecha', 'Tarifa', 'Multiplicador', 'Total', 'Deposito']

    rute_and_name = "/var/www/kernotekv3/static/download/" + session['username'] + "/Reporte Detallado.xlsx"

    book = xlsxwriter.Workbook(rute_and_name)

    sheet = book.add_worksheet()

    sheet.name = "Ventas"


    # FORMATOS DE LOS DATOS
    # color , 'bg_color': '#428BCA'
    string_format = book.add_format({'bold': True,
                                     'font_size': 10,
                                     'font_name': 'Arial',
                                     'align': 'center',
                                     'valign': 'vcenter'})

    num_format = book.add_format({'align': 'center',
                                  'border': 1,
                                  'font_name': 'Arial'})

    dateTime_format = book.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss',
                                       'align': 'center',
                                       'border': 1,
                                       'font_name': 'Arial'})

    cash_format = book.add_format({'num_format': '[$$-80A]#,##0.00;[RED]-[$$-80A]#,##0.00',
                                   'align': 'center',
                                   'border': 1,
                                   'font_name': 'Arial'})

    header_format = book.add_format({'align': 'center',
                                     'border': 1,
                                     'bold': True,
                                     'font_color': '#FFFFFF',
                                     'bg_color': '#428BCA',
                                     'font_name': 'Arial'})


    # INSERTAR IMAGEN CON ESCALA
    sheet.insert_image('A1', 'static/img/reporte.png', {'x_scale': 0.5, 'y_scale': 0.5})

    # DATOS DE LA HOJA
    sheet.merge_range('A4:C4', 'KERNOTEK', string_format)
    sheet.merge_range('E4:F4', 'Fecha: ' + str(dateReport), string_format)
    sheet.merge_range('B6:F6', 'REPORTE DETALLADO.', string_format)
    sheet.merge_range('B8:F8', 'Del ' + startDateReport + ' hrs. AL ' + endDateReport +' hrs.', string_format)


    # FORMATO DE LA TABLA

    # --------<CABEZERAS DINAMICAS>---------------------
    col = ('B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
           'X','Y', 'Z', 'AA', 'AB', 'AC')
    row = 10
    count = 0

    #['Ticket', 'Tarifa', 'Turno', 'Fecha', 'Tarifa', 'Multiplicador', 'Total', 'Deposito']

    cells_format = {'Ticket': {'format': num_format},  # Diccionario con los diferentes tipos de formatos
                    'Turno': {'format': num_format},
                    'Fecha': {'format': dateTime_format},
                    'Tarifa': {'format': cash_format},
                    'Multiplicador': {'format': num_format},
                    'Total': {'format': cash_format},
                    'Deposito': {'format': cash_format}}

    headers = []
    format_columns = []
    for column in columns:  # Cambia el nombre de las columna
        headers.append(column)
        format_columns.append(cells_format[column])

    depositHeaders = ['D 0.5', 'D 1.0', 'D 2.0', 'D 5.0', 'D 10.0', 'D 20.0', 'D 50.0', 'D 100.0', 'D 200.0', 'Cortesía']
    changeHeaders = ['C 0.5', 'C 1.0', 'C 2.0', 'C 5.0', 'C 10.0', 'C 20.0', 'C 50.0', 'C 100.0', 'C 200.0']

    # col = Columna
    # row = fila

    for column in headers:
        sheet.write(col[count] + str(row), column, header_format)  # Inserta las columnas que estan disponibles
        if column == 'Fecha':
            sheet.set_column(col[count] + ':' + col[count], 20)  # TAMAÑO DE LA CELDA FECHA
        count += 1


    inicioDeposito = count  # Indica donde va a a comenzar las cabeceras del deposito

    #  Grega las cabeceras del depostio
    for deposit in depositHeaders:
        sheet.write(col[count] + str(row), deposit, header_format)
        count += 1


    inicioCambio = count  # Indica donde va a a comenzar las cabezeras del deposito

    #  Grega las cabeceras del cambio

    for change in changeHeaders:
        sheet.write(col[count] + str(row), change, header_format)
        count += 1

    sheet.set_column('D:D', 20)  # TAMAÑO DE LA CELDA

    format_columns.append({'format': num_format})
    format_columns.append({'format': num_format})
    format_columns.append({'format': num_format})
    format_columns.append({'format': num_format})

    # DATOS DE LA TABLA
    data = []


    for sells in total_sells:
        data2 = []
        for sell in sells:
            if sell == 0:
                sell = "Token"
            data2.append(sell)
        queryDeposito = "SELECT denomination, quantity from panel_shift_det_den WHERE panelservicesid = " + str(
            sells[0]) + ";"
        queryCambio = "SELECT denomination, quantity from panel_srv_det_den WHERE panelservicesid = " + str(
            sells[0]) + ";"
        totalDeposito = class_db.ejecutar(queryDeposito)  # Guarda la denominacion del deposito de la venta
        totalCambio = class_db.ejecutar(queryCambio)    # Guarda la denominacion del cambio de la venta

        row += 1  # Indica el numero de la fila

        #  crea la cuadricula del deposito y del cambio
        for x in range(0, 19, 1):
            sheet.write(col[inicioDeposito + x] + str(row), "", num_format)

        for deposito in totalDeposito:
            if deposito[0] == 0.5:
                columna = col[inicioDeposito]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 1.0:
                columna = col[inicioDeposito + 1]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 2.0:
                columna = col[inicioDeposito + 2]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 5.0:
                columna = col[inicioDeposito + 3]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 10.0:
                columna = col[inicioDeposito + 4]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 20.0:
                columna = col[inicioDeposito + 5]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 50.0:
                columna = col[inicioDeposito + 6]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 100.0:
                columna = col[inicioDeposito + 7]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 200.0:
                columna = col[inicioDeposito + 8]
                sheet.write(columna + str(row), deposito[1], num_format)
            elif deposito[0] == 0.0:
                columna = col[inicioDeposito + 9]
                sheet.write(columna + str(row), deposito[1], num_format)


        for cambio in totalCambio:
            if cambio[0] == 0.5:
                columna = col[inicioCambio]
                sheet.write(columna + str(row), cambio[1], num_format)
            elif cambio[0] == 1.0:
                columna = col[inicioCambio + 1]
                sheet.write(columna + str(row), cambio[1], num_format)
            elif cambio[0] == 2.0:
                columna = col[inicioCambio + 2]
                sheet.write(columna + str(row), cambio[1], num_format)
            elif cambio[0] == 5.0:
                columna = col[inicioCambio + 3]
                sheet.write(columna + str(row), cambio[1], num_format)
            elif cambio[0] == 10.0:
                columna = col[inicioCambio + 4]
                sheet.write(columna + str(row), cambio[1], num_format)
            elif cambio[0] == 20.0:
                columna = col[inicioCambio + 5]
                sheet.write(columna + str(row), cambio[1], num_format)
            elif cambio[0] == 50.0:
                columna = col[inicioCambio + 6]
                sheet.write(columna + str(row), cambio[1], num_format)
            elif cambio[0] == 100.0:
                columna = col[inicioCambio + 7]
                sheet.write(columna + str(row), cambio[1], num_format)
            elif cambio[0] == 200.0:
                columna = col[inicioCambio + 8]
                sheet.write(columna + str(row), cambio[1], num_format)


        data.append(data2)

    total_registros += len(data)  # indica el fin da la tabla

    #-------<DATOS DE LAS CELADAS>-----------
    tam_table = 'B10:H' + str(total_registros)
    sheet.add_table(tam_table, {'name': 'Reporte de ventas del dia',
                                'banded_columns': True,
                                'header_row': False,
                                'data': data,
                                'autofilter': True,
                                'columns': format_columns})


    book.close()



def reporteTurno(data, date_start, date_end, numTurno):
    startDateReport = date_start.split(' ')
    date = startDateReport[0].split('-')
    startDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ startDateReport[1]
    endDateReport = date_end.split(' ')
    date = endDateReport[0].split('-')
    endDateReport = date[2] +'/'+ date[1] +'/'+ date[0] +' '+ endDateReport[1]

    dateReport = datetime.date.today()
    dateReport = str(dateReport).split('-')
    dateReport = dateReport[2] +'/'+ dateReport[1] +'/'+ dateReport[0] 

    total_sells = data
    total_registros = 10
    date_report = datetime.date.today()

    columns = ['Ticket', 'Fecha', 'Tarifa', 'Multiplicador', 'Total', 'Deposito']

    rute_and_name = "/var/www/kernotekv3/static/download/" + session['username'] + "/Reporte por turno.xlsx"

    book = xlsxwriter.Workbook(rute_and_name)

    sheet = book.add_worksheet()

    sheet.name = "Ventas"


    # FORMATOS DE LOS DATOS
    # color , 'bg_color': '#428BCA'
    string_format = book.add_format({'bold': True,
                                     'font_size': 10,
                                     'font_name': 'Arial',
                                     'align': 'center',
                                     'valign': 'vcenter'})

    num_format = book.add_format({'align': 'center',
                                  'border': 1,
                                  'font_name': 'Arial'})

    cash_format = book.add_format({'num_format': '[$$-80A]#,##0.00;[RED]-[$$-80A]#,##0.00',
                                   'align': 'center',
                                   'border': 1,
                                   'font_name': 'Arial'})

    header_format = book.add_format({'align': 'center',
                                     'border': 1,
                                     'bold': True,
                                     'font_color': '#FFFFFF',
                                     'bg_color': '#428BCA',
                                     'font_name': 'Arial'})


    dateTime_format = book.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss',
                                       'align': 'center',
                                       'border': 1,
                                       'font_name': 'Arial'})


    # INSERTAR IMAGEN CON ESCALA
    sheet.insert_image('A1', 'static/img/reporte.png', {'x_scale': 0.5, 'y_scale': 0.5})

    # DATOS DE LA HOJA
    sheet.merge_range('C4:D4', 'SERVICIO SECA S.A DE C.V', string_format)
    sheet.merge_range('G4:H4', 'Fecha: ' + str(dateReport), string_format)
    sheet.merge_range('C6:H6', 'REPORTE DEL TURNO NÚMERO '+str(numTurno)+'', string_format)
    sheet.merge_range('C8:H8', 'Del ' + startDateReport + ' hrs. AL  ' + endDateReport + ' hrs.', string_format)


    # DATOS DE LA TABLA
    data = []

    for sells in total_sells:
        data2 = []
        for sell in sells:
            if sell == 0:
                sell = "Cortesía"
            data2.append(sell)
        data.append(data2)

    # FORMATO DE LA TABLA

    # --------<CABEZERAS DINAMICAS>---------------------
    col = ('C', 'D', 'E', 'F', 'G', 'H')
    row = 10
    count = 0

    format_columns = []

    for column in columns:
        sheet.write(col[count] + str(row), column, header_format)  # Inserta las columnas que estan disponibles
        count += 1

    sheet.set_column('C:C', 10)
    sheet.set_column('D:D', 20)  # TAMAÑO DE LA CELDA
    sheet.set_column('E:E', 15)
    sheet.set_column('F:F', 20)
    sheet.set_column('G:G', 15)
    sheet.set_column('H:H', 15)
    #-------<DATOS DE LAS CELADAS>-----------

    format_columns.append({'format': num_format})
    format_columns.append({'format': dateTime_format})
    format_columns.append({'format': cash_format})
    format_columns.append({'format': num_format})
    format_columns.append({'format': cash_format})
    format_columns.append({'format': cash_format})

    total_registros += len(data)
    tam_table = 'C10:H' + str(total_registros)

    sheet.add_table(tam_table, {'name': 'Reporte de ventas',
                                'banded_columns': True,
                                'header_row': False,
                                'data': data,
                                'columns': format_columns})

    montos = class_db.montosTurno(numTurno)

    sheet.merge_range('C' + str(len(data) + 12) + ':E' + str(len(data) + 12), 'INFO. MONTO', header_format)
    sheet.merge_range('C' + str(len(data) + 13) + ':D' + str(len(data) + 13), 'Monto Inicial', header_format)

    sheet.merge_range('C' + str(len(data) + 14) + ':D' + str(len(data) + 14), 'Monto Final', header_format)

    sheet.write('E' + str(len(data) + 13), montos[0][0], cash_format)
    sheet.write('E' + str(len(data) + 14), montos[0][1], cash_format)
    book.close()
