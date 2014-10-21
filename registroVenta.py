# -*- coding:utf-8 -*-
__autor__="aramirez"

import datetime
import class_db
import logger

values = []
check_sum = 0
DEBUG = 0



"""
    TABLA DE CODIGOS DE ERROR

    01 - Fin de cadena no encontrado
    02 - Error CHECK SUM
    03 - Corrigiendo el número de ticket
    04 - Total incorrecto
    05 - Cambio Incorrecto 

"""





def main(sell):
    existChange = False
    sell = cleanSell(sell)
    cal_checkSum = 0
    if sell.find('\x02') != 0 or sell.find('\x03') != len(sell) - 1:
        if DEBUG:
            print "Venta sin inicio ni fin de cadena"
        logger.error('01| Venta sin inicio o fin de cadena')
    else:
        sell = sell[1:-1]  # Remueve el inicio y fin de cadena
        get_checkSum = sell[len(sell) - 4:]
        checkSum = int(get_checkSum.lower(), 16)  # Convierte el checkSum a decimal
        sell = sell[ :-4 ]  # Remueve el checkSum de la venta

        # ---- Calcula el checkSum de la venta ----

        for char in sell:
            cal_checkSum += ord(char)

        #  ---- Comprueba que el checkSum este correcto ----

        if cal_checkSum != checkSum:
            if DEBUG:
                print "CheckSum erroneo"
            logger.error("02| Se corrompio el CheckSum ")
        else:
            sell = sell[:-1]  # Elimina la ultima pipa de la venta
            values_sell = sell.split('|')

            # ----  Asignacion de los elementos de la venta ----

            numSerie = values_sell[0]
            shift = values_sell[1]
            dateTime = str(values_sell[2]) + " " + str(values_sell[3])
            datetimesell = datetime.datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
            ticket = values_sell[4]
            status = values_sell[5]
            rate = values_sell[6]
            multiplier = values_sell[7]
            cost = values_sell[8]
            deposit = values_sell[9]
            denomDeposit = values_sell[10]   # Denominación del deposito
            cost_cal = float(rate) * float(multiplier)
            # ---- Verifica que el ticket sea correcto ----

            current_ticket = int(class_db.consultarTicket())  # Culsulta el ultimo ticket registrado

            if int(ticket) > (current_ticket + 1):
                if DEBUG:
                    print "El numero del ticket se corrigio"
                logger.warning('03| Corrigiendo el número de ticket')
                ticket = current_ticket + 1
                
            if int(ticket) == current_ticket or int(ticket) < current_ticket:
                if DEBUG:
                    print "El numero del ticket se corrigio"
                logger.warning('03| Corrigiendo el número de ticket')
                ticket = current_ticket + 1


            # ---- Verifica si el total es correcto ----
            
            if float(cost) != cost_cal:
                if DEBUG:
                    print "El total no es correcto"
                status = "1"
                logger.error('04| El total es incorrecto ticket ' + str(ticket))


            # ---- Verifica si hay cambio y comprueba que sea correcto ----
            # 
            if len(values_sell) == 12:
                existChange = True
                change = values_sell[11]
                #separar_cambio(ticket, cambio)
                total_cambio = float(calcular_cambio(change))
                cambio_trama = float(deposit) - float(cost)
                if total_cambio != cambio_trama:
                    print "*" * 40
                    print "CAMBIO INCORRECTO"
                    print "Cambio calculado ", cambio_trama
                    print "cambio recibido ", total_cambio
                    print "*" * 40
                    status = "1"
                    logger.error('05| Cambio incorrecto ticket ' + str(ticket))


            # ---- Se crean las consultas para el registro a la base de datos ----
       
            panelcat = "INSERT INTO panelcat(shiftno, serialnumber)"\
            "VALUES('" + str(shift) + "', '" + str(numSerie) + "');"

            servicesdetail = "INSERT INTO servicesdetail(rate, multiplier, cost) VALUES(" \
            "'" + str(rate) + "', " \
            "'" + str(multiplier) + "'," \
            "'" + str(cost) + "');"

            panelservices = "INSERT INTO panelservices(cost, deposit, ticket, datetimesell, localshift, status) " \
            "VALUES('" + str(cost) + "'," \
            " '" + str(deposit) + "', " \
            "'" + str(ticket) + "', " \
            "'" + str(datetimesell) + "', " \
            "'" + str(shift) + "'," \
            "'" + str(status) +"');"

            config = "UPDATE config SET no_venta_act = '" + str(ticket) + "' WHERE no_serie_acceso = 1;"

            if DEBUG:
                print panelcat
                print servicesdetail
                print panelservices
                print config


            
            if existChange:
                class_db.insertar_venta(panelcat)
                class_db.insertar_venta(servicesdetail)
                class_db.insertar_venta(panelservices)
                class_db.insertar_venta(config)
                insertDeposit(ticket, denomDeposit)
                insertChange(ticket, change)
            else:
                class_db.insertar_venta(panelcat)
                class_db.insertar_venta(servicesdetail)
                class_db.insertar_venta(panelservices)
                class_db.insertar_venta(config)
                insertDeposit(ticket, denomDeposit)
            


def cleanSell(sell):
    inicio = sell.find('\x02')
    fin = sell.find('\x03')
    trama = sell[inicio:fin + 1]
    return trama

def insertDeposit(ticket, deposit):
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
                 "'" + str(deposit_values[2]) + "', " \
                 "'" + str(amount) + "');"
        if DEBUG:
            print query5
        class_db.insertar_venta(query5)
    return


def insertChange(ticket, cambio):
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
                "'" + str(deposit_values[2]) + "', " \
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
    return total_cambio


"""
if __name__ == '__main__':
    trama = "AC10TX1241213172|1|2014-10-8|10:12:28|1|0|3.00|1|3.00|3.00|M,1.0,1;M,2.0,1|1245"
    cambio = "AC10TX1241213172|1|2014-10-8|10:20:10|1|0|3.00|1|3.00|5.00|M,5.0,1|M,2.0,1|1282"
    token = "AC10TX1241213172|1|2014-10-8|10:56:27|100|0|15.00|1|15.00|0.00|T,0,1|1116"
    cambioIncorrecto = "AC10TX1241213172|1|2014-10-8|14:52:51|1|0|3.00|1|3.00|4.00|M,1.0,2;M,2.0,1|M,1.0,1;M,2.0,1|15CD "
    main(cambioIncorrecto)
"""
