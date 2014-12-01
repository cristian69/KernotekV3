# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import datetime
import class_db


values = []
check_sum = 0
DEBUG = 1


"""
    TABLA DE CODIGOS DE ERROR

    01 - Fin de cadena no encontrado
    02 - Error CHECK SUM
    03 - Corrigiendo el número de ticket
    04 - Total incorrecto
    05 - Cambio Incorrecto 

"""


def main(trama):
    registro_correcto = True
    trama = limpiar_trama(trama)
    check_sum_cal = 0

    if trama.find('\x02') != 0 or trama.find('\x03') != len(
            trama) - 1:  # cambiar a menos dos para comunicarse con el monedero
        print "01 |No se encuentra el inicio o fin de cadena"
        registro_correcto = False
    else:
        trama = trama[1:-1]  # remove byte to start and end
        # print trama
        check_sum = trama[len(trama) - 4:]  # get check sum of string
        check_sum = int(check_sum.lower(), 16)
        trama = trama[:-4]  # remove check sum
        for letra in trama:
            check_sum_cal += ord(letra)
        if check_sum_cal != check_sum:
            print "Error con el check sum"
            registro_correcto = False
        else:
            trama = trama[:-1]
            values = trama.split('|')

            # Asignacion de los elementos de la trama
            No_serie = values[0]
            turno = values[1]
            fecha_hora = str(values[2]) + " " + str(values[3])
            datetimesell = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
            ticket = values[4]
            no_detalle = values[5]
            tarifa = values[6]
            multiplicador = values[7]
            total = values[8]
            deposito = values[9]
            ingreso = values[10]

            total_cal = float(tarifa) * float(multiplicador)

            # Verifica que el número de ticket sea el correcto
            ultimoTicket = int(class_db.consultarTicket())
            if int(ticket) > (ultimoTicket + 1):
                ticket = ultimoTicket + 1

            if int(ticket) == ultimoTicket or int(ticket) < ultimoTicket:
                print "El numero del ticket se corrigio"
                ticket = ultimoTicket + 1

            if float(total) != total_cal:
                print "El total no es correcto"
                #registro_correcto = False
                no_detalle = "1"

            if len(values) == 12:
                        cambio = values[11]
                        #separar_cambio(ticket, cambio)
                        total_cambio = float(calcular_cambio(cambio))
                        cambio_trama = float(deposito) - float(total)
                        if total_cambio != cambio_trama:
                            no_detalle = "1"
                            print "*" * 40
                            print "CAMBIO INCORRECTO"
                            print "Cambio calculado ", cambio_trama
                            print "cambio recibido ", total_cambio
                            print "*" * 40

            if registro_correcto:  # inserta la venta si todos los datos son correctos
                query = "INSERT INTO panelcat(shiftno, serialnumber)"\
                "VALUES('" + str(turno) + "', '" + str(No_serie) + "');"

                query2 = "INSERT INTO servicesdetail(rate, multiplier, cost) VALUES(" \
                         "'" + str(tarifa) + "', " \
                                             "'" + str(multiplicador) + "'," \
                                                                        "'" + str(total) + "');"

                query3 = "INSERT INTO panelservices(cost, deposit, ticket, datetimesell, localshift, status) " \
                         "VALUES('" + str(total) + "'," \
                                                   " '" + str(deposito) + "', " \
                                                                          "'" + str(ticket) + "', " \
                                                                                              "'" + str(
                    datetimesell) + "', " \
                                    "'" + str(turno) + "');"

                query4 = "UPDATE config SET no_venta_act = '" + str(ticket) + "' WHERE no_serie_acceso = 1;"  #Actualiza el número de ticket de la tabla config

                if DEBUG:
                    print query
                    print query2
                    print query3
                    print query4

                if len(values) == 12:
                    class_db.insertar_venta(query)
                    class_db.insertar_venta(query2)
                    class_db.insertar_venta(query3)
                    class_db.insertar_venta(query4)
                    separar_deposito(ticket, ingreso)
                    separar_cambio(ticket, cambio)
                else:
                    class_db.insertar_venta(query)
                    class_db.insertar_venta(query2)
                    class_db.insertar_venta(query3)
                    class_db.insertar_venta(query4)
                    separar_deposito(ticket, ingreso)

    return registro_correcto


def separar_deposito(ticket, deposit):
    deposit = deposit.split(';')
    for elements in deposit:
        elements = elements.split(',')
        deposit_values = []
        for i in elements:
            deposit_values.append(i)
        amount = float(deposit_values[1]) * float(deposit_values[2])
        query5 = "INSERT INTO panel_shift_det_den(panelservicesid, denomination, typecurr, quantity, amount) " \
                 "VALUES('" + str(ticket) + "', " \
                                            "'" + str(deposit_values[1]) + "', " \
                                                                           "'" + str(deposit_values[0]) + "', " \
                                                                                                          "'" + str(
            deposit_values[2]) + "', " \
                                 "'" + str(amount) + "');"
        if DEBUG:
            print query5
        class_db.insertar_venta(query5)
    return


def separar_cambio(ticket, cambio):
    cambio = cambio.split(';')
    for elements in cambio:
        elements = elements.split(',')
        deposit_values = []
        for i in elements:
            deposit_values.append(i)
        amount = float(deposit_values[1]) * float(deposit_values[2])
        query = "INSERT INTO panel_srv_det_den(panelservicesid, denomination, typecurr, quantity, amount) " \
                "VALUES('" + str(ticket) + "', " \
                                           "'" + str(deposit_values[1]) + "', " \
                                                                          "'" + str(deposit_values[0]) + "', " \
                                                                                                         "'" + str(
            deposit_values[2]) + "', " \
                                 "'" + str(amount) + "');"
        if DEBUG:
            print query
        class_db.insertar_venta(query)
    return


def calcular_cambio(change):
    total_cambio = 0
    change = change.split(';')
    for elements in change:
        elements = elements.split(',')
        total_cambio += float(elements[1]) * float(elements[2])
        change_values = []
        for i in elements:
            change_values.append(i)
    # print "Total Cambio ", str(total_cambio)
    return total_cambio


def limpiar_trama(trama):
    inicio = trama.find('\x02')
    fin = trama.find('\x03')
    trama = trama[inicio:fin + 1]
    return trama



if __name__ == '__main__':
    trama = "AC10TX1241213172|1|2014-10-8|10:12:28|1|0|3.00|1|3.00|3.00|M,1.0,1;M,2.0,1|1245"
    cambio = "AC10TX1241213172|1|2014-10-8|10:20:10|1|0|3.00|1|3.00|5.00|M,5.0,1|M,2.0,1|1282"
    token = "AC10TX1241213172|1|2014-10-8|10:56:27|100|0|15.00|1|15.00|0.00|T,0,1|1116"
    cambioIncorrecto = "AC10TX1241213172|1|2014-10-8|14:52:51|1|0|3.00|1|3.00|4.00|M,1.0,2;M,2.0,1|M,1.0,1;M,2.0,1|15CD "
    main(cambio)

