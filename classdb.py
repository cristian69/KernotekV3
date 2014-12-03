#-*- coding: utf-8 -*-
from distutils.archive_util import make_tarball

__author__ = 'adrian'
from flaskext.mysql import MySQL
import flask
from libgral import ObtenerFecha, FechaHora
import sys
from flask import session

db = None
cursor = None
mysql = MySQL()

try:
    app = flask.Flask(__name__)
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    app.config['MYSQL_DATABASE_DB'] = 'kernotek'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
    db = mysql.connect()
    cursor = db.cursor()
except:
    print "ERROR NO SE PUEDE ACCESAR A LA BASE DE DATOS \nREVISAR CONFIGURACION"
    sys.exit(0)


def makeConnection():
    global db 
    global cursor
    db = mysql.connect()
    cursor = db.cursor()


def closeConnection():
    global db
    global cursor
    db.close()
    cursor.close()


#########################################################
#                                                       #
#                     REPORTES                          #
#                                                       #
#########################################################

def consultaColumnas():
    query = "SELECT conf_report FROM users WHERE username = '"+session['username']+"';"
    makeConnection()
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    return data[0]


def columnas_habilitadas():
    verColumnas = []
    contador = 0
    nomColumnas = ['ticket', 'localshift', 'datetimesell', 'no_detalle', 'rate', 'deposit']
    makeConnection()
    query = "SELECT conf_report FROM users WHERE username = '"+session['username']+"';"
    cursor.execute(query)
    columnas = cursor.fetchone()
    columnas = str(columnas[0]).split('-')
    closeConnection()
    for estado in columnas:
        if estado == '1':
            verColumnas.append(nomColumnas[contador])
        contador += 1
    return verColumnas


def modificar_reporte(nuevoEstado):
    makeConnection()
    query = "UPDATE users SET  conf_report = '"+nuevoEstado+"' WHERE username = '"+session['username']+"';"
    cursor.execute(query)
    db.commit()
    closeConnection()


def total_registros(dateStart, dateEnd, inicio):
    makeConnection()
    query = "SELECT count(*) FROM (SELECT ticket FROM panelservices "\
            "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"', \"%Y-%m-%d %H:%i:%s\") order by datetimesell DESC LIMIT "+str(inicio)+", 500) as alias;"
    # query = "SELECT ticket FROM panelservices " \
    #             "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"', \"%Y-%m-%d %H:%i:%s\") ORDER BY datetimesell DESC LIMIT "+str(inicio)+", 500;"
    cursor.execute(query)
    # print "-" * 40
    # print query
    # print "-" * 40
    num_registros = cursor.fetchall()
    closeConnection()
    return num_registros[0][0]

"""
def totalRegistrosTurno(turno, inicio):
    makeConnection()
    query = "SELECT COUNT(*)FROM panelservices INNER JOIN servicesdetail ON panelservices.panelservicesid = servicesdetail.servicesdetailid WHERE localshift = '1' order by datetimesell desc limit 0,20;"
"""
def paginacion(dateStart, dateEnd, inicio):
    makeConnection()
    query = "SELECT "
    columns = columnas_habilitadas()

    # agrega las columnas que se estan activas para el reporte
    for columna in columns:
        query += columna + ", "

    if dateEnd == None or dateStart == None:
        data = None
        return data
    else:
        makeConnection()
        query = query[:-2] + " FROM panelservices INNER JOIN servicesdetail ON panelservices.panelservicesid = servicesdetail.servicesdetailid " \
                "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"', \"%Y-%m-%d %H:%i:%s\") ORDER BY datetimesell DESC LIMIT "+str(inicio)+", 50;"
        cursor.execute(query)
        data = cursor.fetchall()
        closeConnection()
        return data

#============================= REPORTE ESPECIFICO ===========================================

def reporte_especifico(dateStart, dateEnd):
    makeConnection()
    query = "SELECT "
    columns = columnas_habilitadas()
    # agrega las columnas que se estan activas para el reporte
    for columna in columns:
        query += columna + ", "
    if dateEnd == None or dateStart == None:
        data = None
        return data
    else:
        makeConnection()

        query = query[:-2] + " FROM panelservices INNER JOIN servicesdetail ON panelservices.panelservicesid = servicesdetail.servicesdetailid " \
                "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"',\"%Y-%m-%d %H:%i:%s\") ORDER BY datetimesell;"
        cursor.execute(query)
        data = cursor.fetchall()
        closeConnection()
        return data

#============================= REPORTE GENERAL ===========================================


def reporte_general(fechaInicio, fechaFin):
    makeConnection()
    query = "SELECT cost, count(cost), SUM(cost) FROM panelservices " \
            " WHERE  deposit != 0 AND updatetime BETWEEN STR_TO_DATE('"+fechaInicio+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+fechaFin+"', \"%Y-%m-%d %H:%i:%s\") GROUP BY cost ;"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data


# SE VERIFICA QUE COLUMNAS SE PUDEN VISUALIZAR EN EL REPORTE
def state_report_gral():
    makeConnection()
    query = "SELECT * FROM conf_report_gral;"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data


def totales(fechaInicio, fechaFin):
    makeConnection()
    query = "SELECT COUNT(cost), SUM(cost) FROM panelservices WHERE  deposit != 0 AND updatetime BETWEEN STR_TO_DATE('"+fechaInicio+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+fechaFin+"', \"%Y-%m-%d %H:%i:%s\");"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data

#============================= REPORTE DETALLADO ===========================================
def reportDetallado(dateStart, dateEnd):
    makeConnection()
    query = "SELECT ticket, localshift, datetimesell, rate,multiplier, servicesdetail.cost, deposit " \
            "FROM panelservices INNER JOIN servicesdetail " \
            "ON panelservices.panelservicesid = servicesdetail.servicesdetailid " \
            "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"', \"%Y-%m-%d %H:%i:%s\") ORDER BY datetimesell;"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data

#============================= REPORTE POR TURNO ===========================================
def turnosDisponibles(startDate, endDate):
    makeConnection()
    query = "SELECT shiftno, datestart, dateend FROM panelshifthead WHERE dateend BETWEEN STR_TO_DATE('"+startDate+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+endDate+"', \"%Y-%m-%d %H:%i:%s\");"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data


def reporteTurno(numTurno):
    makeConnection()
    query = "SELECT ticket, datetimesell, rate, multiplier, servicesdetail.cost, deposit " \
            "FROM panelservices INNER JOIN servicesdetail " \
            "ON panelservices.panelservicesid = servicesdetail.servicesdetailid " \
            "WHERE localshift = '"+numTurno+"';"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data


def montosTurno(numTurno):
    makeConnection()
    query = "SELECT amountini, amountend FROM panelshifthead WHERE shiftno = "+numTurno+""
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data

def reporteTurnoPaginacion(turno, index):
    makeConnection()
    query = "SELECT ticket, datetimesell, rate, multiplier, servicesdetail.cost, deposit"\
    " FROM panelservices INNER JOIN servicesdetail ON panelservices.panelservicesid = servicesdetail.servicesdetailid "\
    "WHERE localshift = '"+str(turno)+"' order by datetimesell desc limit "+str(index)+",50;"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data



#########################################################
#                                                       #
#                     TURNOS                            #
#                                                       #
#########################################################



# Consulta si hay un corte de turno desde la pagina
def consultarCorteTurno():
    makeConnection()
    query = "SELECT hacer_corte_turno FROM config"
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    data = str(data[0])
    if data == '0':
        return False
    else:
        return True

# Indica que se ha realizado un corte de turno desde la página
def activarCorteTurno():
    makeConnection()
    query = "UPDATE config set hacer_corte_turno = '1'"
    cursor.execute(query)
    db.commit()
    closeConnection()


# Registra que no hay corte de turno pendiente
def desactivarCorteTurno():
    makeConnection()
    query = "UPDATE config set hacer_corte_turno = '0'"
    cursor.execute(query)
    db.commit()
    closeConnection()


# regresa que tipo de corte es Automatico o manual
def tipoCorte():
    makeConnection()
    query = "SELECT tipo_corte FROM config"
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    data = data[0]

    if data == '0': 
        return "manual"
    else:
        return "automatico"

# Registra el intervalo de tiempo del corte automatico
def tiempoCorteAuto(tiempo):
    makeConnection()
    query = "UPDATE config set tiempo_corte = '"+str(tiempo)+"'"
    cursor.execute(query)
    db.commit()
    closeConnection()


# Registra el tipo de tiempo del corte automatico
def tipoTiempoAutomatico(tipoTiempo):
    makeConnection()
    query = "UPDATE config set corte_automatico =  '"+str(tipoTiempo)+"'"
    cursor.execute(query)
    db.commit()
    closeConnection()


# Consulta el tipo de tiempo del corte automatico
def consultarTipoTiempo():
    makeConnection()
    query = "SELECT corte_automatico FROM config"
    cursor.execute(query)
    data =  cursor.fetchall()
    data = data[0][0]
    closeConnection()
    return data

# consulta el tiempo del corte automatico
def consultarTiempo():
    makeConnection()
    query = "SELECT tiempo_corte FROM config"
    cursor.execute(query)
    data = cursor.fetchall()
    data = data[0][0]
    return data

# registra la hora del proximo corte solo se utiliza para cada determinada hora
def registroProxCorteAuto(fecha):
    makeConnection()
    query ="UPDATE  config SET prox_corte_auto = '"+str(fecha)+"'"
    cursor.execute(query)
    db.commit()
    closeConnection()

def consultProxCorte():
    makeConnection()
    query = "SELECT prox_corte_auto FROM config"
    cursor.execute(query)
    data = cursor.fetchall()
    data = data[0][0]
    closeConnection()
    return data

def cambiarTipoCorte(tipoCorte):
    makeConnection()
    query = "UPDATE config set tipo_corte = '"+tipoCorte+"'"
    cursor.execute(query)
    db.commit()
    closeConnection()


def turnoActual():
    makeConnection()
    query = "SELECT MAX(shiftno) FROM panelshifthead"
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    return data[0]

def ultimoTurno():
    makeConnection()
    query = "SELECT dateend from panelshifthead order by dateend DESC limit 1;"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    if len(data) == 0:
        return ""
    return data[0][0]

def datosTurnoActual():
    makeConnection()
    query = "SELECT shiftno, datestart FROM panelshifthead WHERE shiftno = (SELECT MAX(shiftno) FROM panelshifthead);"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data[0]

def ventasTurno(numTurno):
    makeConnection()
    query = "SELECT COUNT(localshift) FROM panelservices WHERE localshift = "+numTurno+";"
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    return data[0]

def acumuladoTurno(numTurno):
    makeConnection()
    query = "SELECT SUM(cost) FROM panelservices WHERE deposit != 0 AND localshift = "+numTurno+";"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    if str(data[0][0]) == 'None':
        return float(0)
    else:
        return float(data[0][0])

# Crea un nuevo turno
def iniciarTurno(numTurno, fechaIncio, montoInicial):
    makeConnection()
    query = "INSERT INTO panelshifthead(shiftno, datestart, amountini) VALUES("+str(numTurno)+", '"+fechaIncio+"', "+str(montoInicial)+");"
    cursor.execute(query)
    db.commit()
    closeConnection()


def corteTurno(montoFinal):    
    turnoActivo = turnoActual()
    fechaFin = FechaHora()
    montoFinal = montoFinal   #Cantidad de dinero que tiene al finalizar el turno activo
    nuevoTurno = int(turnoActivo) + 1
    makeConnection()
    queryCorteTurno = "UPDATE panelshifthead SET dateend = '"+str(fechaFin)+"', amountend = "+str(montoFinal)+" WHERE shiftno = "+str(turnoActivo)+""
   
    cursor.execute(queryCorteTurno)
    db.commit()
    closeConnection()

    iniciarTurno(nuevoTurno, fechaFin, montoFinal) # Registra el nuevo turno

    # Actualiza la tabla de config con el numero de turno activo
    makeConnection()
    query = "UPDATE config set shift_no_act = "+str(nuevoTurno)+""
    cursor.execute(query)
    db.commit()
    closeConnection()

#########################################################
#                                                       #
#                     USUARIOS                          #
#                                                       #
#########################################################



def nombre_completo_usuario(username):
    makeConnection()
    query = "select nombre, appaterno, apmaterno from users where username='"+username+"'"
    cursor.execute(query)
    data = cursor.fetchone()
    nombre_usuario = ' '.join(str(x) for x in data)
    closeConnection()
    return nombre_usuario




def validar_usuario(user, password):
    makeConnection()
    query ="SELECT username, typeuser FROM users WHERE username = '"+user+"' AND AES_DECRYPT(password, 'I[t_[0n5u/71n&') = '"+password+"' AND activa = 1;"
    if query.upper().startswith('SELECT'):
        cursor.execute(query)
        data = cursor.fetchone()
        closeConnection()
        return data
    closeConnection()


#########################################################
#                                                       #
#                       HOME                            #
#                                                       #
#########################################################


def ventasDia():
    makeConnection()
    query = "select day(datetimesell),sum(cost)from panelservices where not deposit=0 and datetimesell > date_sub(curdate(), interval 7 day) group by day(datetimesell) desc;" 
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data

def ventasSemana():
    makeConnection()
    query = "select week(datetimesell),sum(cost)from panelservices where not deposit=0 and datetimesell > date_sub(curdate(), interval 7 week) group by {fn week(datetimesell)} desc;" 
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data

def ventasMes():
    makeConnection()
    query = "select month(datetimesell),sum(cost)from panelservices where not deposit=0 and datetimesell > date_sub(curdate(), interval 7 month) group by month(datetimesell);"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data

def ticket_actual():
    makeConnection()
    query = "SELECT ticket FROM panelservices WHERE panelservicesid = (SELECT MAX(panelservicesid) FROM panelservices);"
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    if not data:
        return 0
    else:
        data = data[0]
        return data


def ventas_del_dia():
    makeConnection()
    total = '$ '
    fecha_inicio = ObtenerFecha()
    fecha2 = fecha_inicio.split('-')
    fecha2[0] = int(fecha2[0]) + 1
    fecha_fin = '-'.join(str(x) for x in fecha2)
    query = "SELECT SUM(cost) FROM panelservices  WHERE  deposit != 0 AND updatetime BETWEEN '"+fecha_inicio+"' AND '"+fecha_fin+"';"
    cursor.execute(query)
    data = cursor.fetchone()
    data = data[0]
    closeConnection()
    if data:
        total += str(data) + '0'
        return total
    else:
        return 'No hay ventas hasta ahora'





#########################################################
#                                                       #
#                       SISTEMA                         #
#                                                       #
#########################################################

def cambiarTarifa(tarifa):
    makeConnection()
    query = "UPDATE config SET rate = '"+tarifa+"';"
    cursor.execute(query)
    db.commit()
    closeConnection() 


def cambiarTiempoApertura(tiempo):
    makeConnection()
    query = "UPDATE config SET t_apertura = '"+tiempo+"';"
    cursor.execute(query)
    db.commit()
    closeConnection()


def numSerieAcceso():
    makeConnection()
    query = "SELECT no_serie_acceso FROM config"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    data = data[0][0]
    return data

# Cosulta si el socket de python esta activo
def consultaSocketPython():
    query = "SELECT socketPython FROM config;"
    makeConnection()
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    if data[0] == 1:
        return "Activo"
    else:
        return "Inactivo"


# Consulta si el socket de C esta activo
def consultaSocketC():
    query = "SELECT socketC FROM config;"
    makeConnection()
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    if data[0] == 1:
        return "Activo"
    else:
        return "Inactivo"



# Registra el estado de socket python 
def estadoSocketPython(estado):
    query = "UPDATE config SET socketPython= '"+estado+"';"
    makeConnection()
    cursor.execute(query)
    db.commit()
    closeConnection()


#Registra el estado del socket C
def estadoSocketC(estado):
    query = "UPDATE config SET socketC = '"+estado+"';"
    makeConnection()
    cursor.execute(query)
    db.commit()
    closeConnection()


def ticket():
    query = "SELECT no_venta_act FROM config;"
    makeConnection()
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    return data[0]


def tarifa():
    query = "SELECT rate FROM config;"
    makeConnection()
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    return data[0]


def consultarTarifa():
    query = "SELECT cost FROM panelservices WHERE panelservicesid = (SELECT MAX(panelservicesid) FROM panelservices);"
    makeConnection()
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    return data[0]

def tiempo_apertura():
    makeConnection()
    query = "SELECT t_apertura FROM config;"
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    data = data[0]
    return data


# PENDIENTE REVISAR 
def Num_serie():
    query = "SELECT serialnumber FROM panelcat;"
    makeConnection()
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    return data


def estado_sistema():
    makeConnection()
    query = "SELECT no_serie_acceso, rate, t_apertura, no_venta_act, shift_no_act, no_serie_payout, no_serie_hopper from config;"
    cursor.execute(query)
    data = cursor.fetchone()
    closeConnection()
    rate = data[0]
    return data


def cambiar_estado_sistema(numSerie, tariafa, t_apertura, num_payout, num_hopper):
    makeConnection()
    query = "UPDATE config SET " \
            "no_serie_acceso = '"+numSerie+"', " \
            "rate = '"+tariafa+"', " \
            "t_apertura = '"+t_apertura+"', " \
            "no_serie_payout = '"+num_payout+"', " \
            "no_serie_hopper = '"+num_hopper+"';"
    cursor.execute(query)
    db.commit()
    closeConnection()


def canales_monedero():
    makeConnection()
    query = "SELECT canal, estado FROM canales_hopper"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data


def canales_billetero():
    makeConnection()
    query = "SELECT canal, estado FROM canales_payout"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data


#########################################################
#                                                       #
#                       VENTA                           #
#                                                       #
#########################################################


def consultarTicket():
    makeConnection()
    query = "SELECT no_venta_act FROM config"
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data[0][0]

def idpanelServices():
    makeConnection()
    query = "SELECT servicesdetailid from servicesdetail  ORDER BY servicesdetailid DESC limit 1;"
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) == 0:
        data = '0'
    else:
        data = data[0][0]
        closeConnection()
        data = int(data) +  1
    return data


def insertar_venta(query):
    makeConnection()
    cursor.execute(query)
    db.commit()
    closeConnection()

#########################################################
#                                                       #
#                    BITACORA                           #
#                                                       #
#########################################################


def registro_bitacora(usuario, inicio_sesion, fin_sesion):
    makeConnection()
    query ="INSERT INTO bitacora(username, startsesion, endsesion) VALUES('"+usuario+"'," \
                                                                              " '"+inicio_sesion+"', " \
                                                                              "'"+fin_sesion+"');"
    cursor.execute(query)
    db.commit()
    closeConnection()



def ejecutar(query):
    makeConnection()
    cursor.execute(query)
    data = cursor.fetchall()
    closeConnection()
    return data
