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
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'KERNOTEK'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
    db = mysql.connect()
    cursor = db.cursor()
except:
    print "ERROR NO SE PUEDE ACCESAR A LA BASE DE DATOS \nREVISAR CONFIGURACION"
    sys.exit(0)


def crear_conexion():
    global db 
    global cursor
    db = mysql.connect()
    cursor = db.cursor()


def matar_conexion():
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
    crear_conexion()
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    return data[0]


def columnas_habilitadas():
    verColumnas = []
    contador = 0
    nomColumnas = ['ticket', 'localshift', 'datetimesell', 'no_detalle', 'rate', 'deposit']
    crear_conexion()
    query = "SELECT conf_report FROM users WHERE username = '"+session['username']+"';"
    cursor.execute(query)
    columnas = cursor.fetchone()
    columnas = str(columnas[0]).split('-')
    matar_conexion()
    for estado in columnas:
        if estado == '1':
            verColumnas.append(nomColumnas[contador])
        contador += 1
    return verColumnas


def modificar_reporte(nuevoEstado):
    crear_conexion()
    query = "UPDATE users SET  conf_report = '"+nuevoEstado+"' WHERE username = '"+session['username']+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def total_registros(dateStart, dateEnd, inicio):
    crear_conexion()
    query = "SELECT ticket FROM panelservices " \
                "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"', \"%Y-%m-%d %H:%i:%s\") ORDER BY datetimesell DESC LIMIT "+str(inicio)+", 500;"
    cursor.execute(query)
    num_registros = cursor.fetchall()
    matar_conexion()
    return len(num_registros)


def paginacion(dateStart, dateEnd, inicio):
    crear_conexion()
    query = "SELECT "
    columns = columnas_habilitadas()

    # agrega las columnas que se estan activas para el reporte
    for columna in columns:
        query += columna + ", "

    if dateEnd == None or dateStart == None:
        data = None
        return data
    else:
        crear_conexion()
        query = query[:-2] + " FROM panelservices INNER JOIN servicesdetail ON panelservices.panelservicesid = servicesdetail.servicesdetailid " \
                "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"', \"%Y-%m-%d %H:%i:%s\") ORDER BY datetimesell DESC LIMIT "+str(inicio)+", 50;"
        cursor.execute(query)
        data = cursor.fetchall()
        matar_conexion()
        return data

#============================= REPORTE ESPECIFICO ===========================================

def reporte_especifico(dateStart, dateEnd):
    crear_conexion()
    query = "SELECT "
    columns = columnas_habilitadas()
    # agrega las columnas que se estan activas para el reporte
    for columna in columns:
        query += columna + ", "
    if dateEnd == None or dateStart == None:
        data = None
        return data
    else:
        crear_conexion()

        query = query[:-2] + " FROM panelservices INNER JOIN servicesdetail ON panelservices.panelservicesid = servicesdetail.servicesdetailid " \
                "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"',\"%Y-%m-%d %H:%i:%s\") ORDER BY datetimesell;"
        cursor.execute(query)
        data = cursor.fetchall()
        matar_conexion()
        return data

#============================= REPORTE GENERAL ===========================================


def reporte_general(fechaInicio, fechaFin):
    crear_conexion()
    query = "SELECT cost, count(cost), SUM(cost) FROM panelservices " \
            " WHERE  deposit != 0 AND updatetime BETWEEN STR_TO_DATE('"+fechaInicio+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+fechaFin+"', \"%Y-%m-%d %H:%i:%s\") GROUP BY cost ;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


# SE VERIFICA QUE COLUMNAS SE PUDEN VISUALIZAR EN EL REPORTE
def state_report_gral():
    crear_conexion()
    query = "SELECT * FROM conf_report_gral;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def totales(fechaInicio, fechaFin):
    crear_conexion()
    query = "SELECT COUNT(cost), SUM(cost) FROM panelservices WHERE  deposit != 0 AND updatetime BETWEEN STR_TO_DATE('"+fechaInicio+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+fechaFin+"', \"%Y-%m-%d %H:%i:%s\");"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data

#============================= REPORTE DETALLADO ===========================================
def reportDetallado(dateStart, dateEnd):
    crear_conexion()
    query = "SELECT ticket, localshift, datetimesell, rate,multiplier, servicesdetail.cost, deposit " \
            "FROM panelservices INNER JOIN servicesdetail " \
            "ON panelservices.panelservicesid = servicesdetail.servicesdetailid " \
            "WHERE datetimesell BETWEEN STR_TO_DATE('"+dateStart+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+dateEnd+"', \"%Y-%m-%d %H:%i:%s\") ORDER BY datetimesell;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data

#============================= REPORTE POR TURNO ===========================================
def turnosDisponibles(startDate, endDate):
    crear_conexion()
    query = "SELECT shiftno, datestart, dateend FROM panelshifthead WHERE dateend BETWEEN STR_TO_DATE('"+startDate+"', \"%Y-%m-%d %H:%i:%s\") AND STR_TO_DATE('"+endDate+"', \"%Y-%m-%d %H:%i:%s\");"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def reporteTurno(numTurno):
    crear_conexion()
    query = "SELECT ticket, datetimesell, rate, multiplier, servicesdetail.cost, deposit " \
            "FROM panelservices INNER JOIN servicesdetail " \
            "ON panelservices.panelservicesid = servicesdetail.servicesdetailid " \
            "WHERE localshift = '"+numTurno+"';"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def montosTurno(numTurno):
    crear_conexion()
    query = "SELECT amountini, amountend FROM panelshifthead WHERE shiftno = "+numTurno+""
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data



#########################################################
#                                                       #
#                     LLAVES                            #
#                                                       #
#########################################################


def existeLlave(llave):
    crear_conexion()
    query = "SELECT idKeys FROM llaves WHERE llave = '"+llave+"'"
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        return True

def registroLlave(nombre, apPaterno, apMaterno, grupo, tipoLlave, llave, estado):
    numSerie = numSerieAcceso()
    crear_conexion()
    query = "INSERT INTO llaves(no_serie_acceso, nombre, appaterno, apmaterno, grupo, llave, estado, tipo_llave)"\
            "VALUES('"+str(numSerie)+"', '"+str(nombre)+"', '"+str(apPaterno)+"', '"+str(apMaterno)+"', '"+str(grupo)+"', '"+str(llave)+"',"\
                " '"+str(estado)+"', '"+str(tipoLlave)+"') "
    cursor.execute(query)
    db.commit()
    matar_conexion()


def consultarLlaves(indice):
    crear_conexion()
    query = "SELECT nombre, apPaterno, apMaterno, grupo, tipo_llave, llave, estado FROM llaves limit "+str(indice)+" , 15;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def totalLlaves():
    crear_conexion()
    query = "SELECT nombre, apPaterno, apMaterno, grupo, llave, estado FROM llaves;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def editarLlave(nombre, apPaterno, apMaterno, grupo, tipoLlave, llave, estado):
    crear_conexion()
    query = "UPDATE llaves SET "\
            "nombre = '"+str(nombre)+"', appaterno='"+str(apPaterno)+"', apmaterno='"+str(apMaterno)+"', grupo='"+str(grupo)+"', llave='"+str(llave)+"',"\
                " estado='"+str(estado)+"', tipo_llave='"+str(tipoLlave)+"' WHERE llave= '"+str(llave)+"'"
    
    cursor.execute(query)
    db.commit()
    matar_conexion()

def eliminarLlave(codigoLlave):
    crear_conexion()
    query = "DELETE FROM llaves WHERE llave = '"+str(codigoLlave)+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion()

#########################################################
#                                                       # 
#                     CERRADURA                         #
#                                                       #
#########################################################

# Registra el estado de la cerradura
def estadoCerradura(estado):
    crear_conexion()
    query = "UPDATE config set cerradura = '"+str(estado)+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion()
  
 
# Consulta el estado del escrip de la cerradura 
def consultarCerradura():
    crear_conexion()
    query = "SELECT cerradura FROM config;"
    cursor.execute(query)
    data =  cursor.fetchall()
    matar_conexion()
    data = data[0][0]
    if data == 1:
        return "Activo"
    else:
        return "Inactivo"


def consultKey(key):
    crear_conexion()
    query = "SELECT estado FROM llaves WHERE llave = '"+key+"';"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    if len(data) != 0:
        data = data[0][0]
        if data == 'Activa':
            return True
    return False


#########################################################
#                                                       #
#                     TURNOS                            #
#                                                       #
#########################################################



# Coculta si hay un corte de turno desde la pagina
def consultarCorteTurno():
    crear_conexion()
    query = "SELECT hacer_corte_turno FROM config"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    data = str(data[0])
    if data == '0':
        return False
    else:
        return True

# Indica que se ha realizado un corte de turno desde la página
def activarCorteTurno():
    crear_conexion()
    query = "UPDATE config set hacer_corte_turno = '1'"
    cursor.execute(query)
    db.commit()
    matar_conexion()


# Registra que no hay corte de turno pendiente
def desactivarCorteTurno():
    crear_conexion()
    query = "UPDATE config set hacer_corte_turno = '0'"
    cursor.execute(query)
    db.commit()
    matar_conexion()


# regresa que tipo de corte es Automatico o manual
def tipoCorte():
    crear_conexion()
    query = "SELECT tipo_corte FROM config"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    data = data[0]

    if data == '0': 
        return "manual"
    else:
        return "automatico"

# Registra el intervalo de tiempo del corte automatico
def tiempoCorteAuto(tiempo):
    crear_conexion()
    query = "UPDATE config set tiempo_corte = '"+str(tiempo)+"'"
    cursor.execute(query)
    db.commit()
    matar_conexion()


# Registra el tipo de tiempo del corte automatico
def tipoTiempoAutomatico(tipoTiempo):
    crear_conexion()
    query = "UPDATE config set corte_automatico =  '"+str(tipoTiempo)+"'"
    cursor.execute(query)
    db.commit()
    matar_conexion()


# Consulta el tipo de tiempo del corte automatico
def consultarTipoTiempo():
    crear_conexion()
    query = "SELECT corte_automatico FROM config"
    cursor.execute(query)
    data =  cursor.fetchall()
    data = data[0][0]
    matar_conexion()
    return data

# consulta el tiempo del corte automatico
def consultarTiempo():
    crear_conexion()
    query = "SELECT tiempo_corte FROM config"
    cursor.execute(query)
    data = cursor.fetchall()
    data = data[0][0]
    return data

# registra la hora del proximo corte solo se utiliza para cada determinada hora
def registroProxCorteAuto(fecha):
    crear_conexion()
    query ="UPDATE  config SET prox_corte_auto = '"+str(fecha)+"'"
    cursor.execute(query)
    db.commit()
    matar_conexion()

def consultProxCorte():
    crear_conexion()
    query = "SELECT prox_corte_auto FROM config"
    cursor.execute(query)
    data = cursor.fetchall()
    data = data[0][0]
    matar_conexion()
    return data

def cambiarTipoCorte(tipoCorte):
    crear_conexion()
    query = "UPDATE config set tipo_corte = '"+tipoCorte+"'"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def turnoActual():
    crear_conexion()
    query = "SELECT MAX(shiftno) FROM panelshifthead"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    return data[0]


def datosTurnoActual():
    crear_conexion()
    query = "SELECT shiftno, datestart FROM panelshifthead WHERE shiftno = (SELECT MAX(shiftno) FROM panelshifthead);"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data[0]

def ventasTurno(numTurno):
    crear_conexion()
    query = "SELECT COUNT(localshift) FROM panelservices WHERE localshift = "+numTurno+";"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    return data[0]

def acumuladoTurno(numTurno):
    crear_conexion()
    query = "SELECT SUM(cost) FROM panelservices WHERE deposit != 0 AND localshift = "+numTurno+";"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    if data[0][0] == 'None':
        return float(0)
    else:
        return float(data[0][0])

# Crea un nuevo turno
def iniciarTurno(numTurno, fechaIncio, montoInicial):
    crear_conexion()
    query = "INSERT INTO panelshifthead(shiftno, datestart, amountini) VALUES("+str(numTurno)+", '"+fechaIncio+"', "+str(montoInicial)+");"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def corteTurno(montoFinal):    
    turnoActivo = turnoActual()
    fechaFin = FechaHora()
    montoFinal = montoFinal   #Cantidad de dinero que tiene al finalizar el turno activo
    nuevoTurno = int(turnoActivo) + 1
    crear_conexion()
    queryCorteTurno = "UPDATE panelshifthead SET dateend = '"+str(fechaFin)+"', amountend = "+str(montoFinal)+" WHERE shiftno = "+str(turnoActivo)+""
   
    cursor.execute(queryCorteTurno)
    db.commit()
    matar_conexion()

    iniciarTurno(nuevoTurno, fechaFin, montoFinal) # Registra el nuevo turno

    # Actualiza la tabla de config con el numero de turno activo
    crear_conexion()
    query = "UPDATE config set shift_no_act = "+str(nuevoTurno)+""
    cursor.execute(query)
    db.commit()
    matar_conexion()

#########################################################
#                                                       #
#                     USUARIOS                          #
#                                                       #
#########################################################


def consultarPassword(username):
    crear_conexion()
    query = "SELECT AES_DECRYPT(password, 'I[t_[0n5u/71n&') AS password FROM users WHERE username='"+username+"';"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    data = data[0]
    return data


def datos_perfil(username):
    crear_conexion()
    query = "SELECT nombre, appaterno, apmaterno, username, email, typeuser FROM users WHERE username = '"+username+"'"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    return data


def nombre_completo_usuario(username):
    crear_conexion()
    query = "select nombre, appaterno, apmaterno from users where username='"+username+"'"
    cursor.execute(query)
    data = cursor.fetchone()
    nombre_usuario = ' '.join(str(x) for x in data)
    matar_conexion()
    return nombre_usuario


def restablecer_password(user_name, password):
    crear_conexion()
    query = "UPDATE users set password = AES_ENCRYPT('"+password+"', 'I[t_[0n5u/71n&') WHERE username = '"+user_name+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def validar_usuario(user, password):
    crear_conexion()
    query ="SELECT username, typeuser FROM users WHERE username = '"+user+"' AND AES_DECRYPT(password, 'I[t_[0n5u/71n&') = '"+password+"' AND activa = 1;"
    if query.upper().startswith('SELECT'):
        cursor.execute(query)
        data = cursor.fetchone()
        matar_conexion()
        return data
    matar_conexion()


def nuevo_usuario(nombre, appaterno, apmaterno, username, password, email, typeuser):
    crear_conexion()
    query = "INSERT INTO users(nombre, appaterno, apmaterno, username, password , email, typeuser, conf_report) VALUES(" \
            "'"+ nombre +"', " \
            "'"+ appaterno+"', " \
            "'"+apmaterno+"', " \
            "'"+username+"', " \
            "AES_ENCRYPT('"+password+"', 'I[t_[0n5u/71n&'), " \
            "'"+email+"', " \
            "'"+typeuser+"', " \
            "'1-1-1-0-1-1');"  # Configuración del reporte cada uno representa el estado de la columna
    cursor.execute(query)
    db.commit()
    matar_conexion()


def eliminar_usuario(username):
    crear_conexion()
    query = "DELETE FROM users WHERE username = '" +username+ "';"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def validar_username(username):
    crear_conexion()
    query = "SELECT username FROM users WHERE username = '" +username+"';"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    if len(data) == 0:
        return True
    else:
        return False


def ver_usuarios(indice):
    crear_conexion()
    query = "SELECT nombre, appaterno, apmaterno, username, typeuser, email, alta, activa FROM users WHERE username NOT IN ('admin') limit "+str(indice)+", 15;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def totalUsuarios():
    crear_conexion()
    query = "SELECT nombre, appaterno, apmaterno, username, typeuser, email, alta, activa FROM users;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def ver_usuarios_inactivos(indice):
    crear_conexion()
    query = "SELECT nombre, appaterno, apmaterno, username, typeuser, email, alta FROM users WHERE activa = 0 limit "+str(indice)+", 15;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def usuarioInacticvos():
    crear_conexion()
    query = "SELECT nombre, appaterno, apmaterno, username, typeuser, email, alta FROM users WHERE activa = 0;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def modificarUsuario(username, datos):
    crear_conexion()
    query = "UPDATE users SET nombre = '"+datos['nombre']+"', appaterno = '"+datos['appaterno']+"', apmaterno = '"+datos['apmaterno']+"', email = '"+datos['email']+"' " \
            "WHERE username = '"+username+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def activarCuenta(username):
    crear_conexion()
    query = "UPDATE users SET activa = 1 WHERE username = '"+username+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion()

#########################################################
#                                                       #
#                       HOME                            #
#                                                       #
#########################################################


def ventasDia():
    crear_conexion()
    query = "select day(datetimesell),sum(cost)from panelservices where not deposit=0 and datetimesell > date_sub(curdate(), interval 7 day) group by day(datetimesell) desc;" 
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data

def ventasSemana():
    crear_conexion()
    query = "select week(datetimesell),sum(cost)from panelservices where not deposit=0 and datetimesell > date_sub(curdate(), interval 7 week) group by {fn week(datetimesell)} desc;" 
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data

def ventasMes():
    crear_conexion()
    query = " select month(datetimesell),sum(cost)from panelservices where not deposit=0 and datetimesell > date_sub(curdate(), interval 1 month) group by month(datetimesell) desc;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data

def ticket_actual():
    crear_conexion()
    query = "SELECT ticket FROM panelservices WHERE panelservicesid = (SELECT MAX(panelservicesid) FROM panelservices);"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    if not data:
        return 0
    else:
        data = data[0]
        return data


def ventas_del_dia():
    crear_conexion()
    total = '$ '
    fecha_inicio = ObtenerFecha()
    fecha2 = fecha_inicio.split('-')
    fecha2[0] = int(fecha2[0]) + 1
    fecha_fin = '-'.join(str(x) for x in fecha2)
    query = "SELECT SUM(cost) FROM panelservices  WHERE  deposit != 0 AND updatetime BETWEEN '"+fecha_inicio+"' AND '"+fecha_fin+"';"
    cursor.execute(query)
    data = cursor.fetchone()
    data = data[0]
    matar_conexion()
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
    crear_conexion()
    query = "UPDATE config SET rate = '"+tarifa+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion() 


def cambiarTiempoApertura(tiempo):
    crear_conexion()
    query = "UPDATE config SET t_apertura = '"+tiempo+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def numSerieAcceso():
    crear_conexion()
    query = "SELECT no_serie_acceso FROM config"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    data = data[0][0]
    return data

# Cosulta si el socket de python esta activo
def consultaSocketPython():
    query = "SELECT socketPython FROM config;"
    crear_conexion()
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    if data[0] == 1:
        return "Activo"
    else:
        return "Inactivo"


# Consulta si el socket de C esta activo
def consultaSocketC():
    query = "SELECT socketC FROM config;"
    crear_conexion()
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    if data[0] == 1:
        return "Activo"
    else:
        return "Inactivo"



# Registra el estado de socket python 
def estadoSocketPython(estado):
    query = "UPDATE config SET socketPython= '"+estado+"';"
    crear_conexion()
    cursor.execute(query)
    db.commit()
    matar_conexion()


#Registra el estado del socket C
def estadoSocketC(estado):
    query = "UPDATE config SET socketC = '"+estado+"';"
    crear_conexion()
    cursor.execute(query)
    db.commit()
    matar_conexion()


def ticket():
    query = "SELECT no_venta_act FROM config;"
    crear_conexion()
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    return data[0]


def tarifa():
    query = "SELECT rate FROM config;"
    crear_conexion()
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    return data[0]


def consultarTarifa():
    query = "SELECT cost FROM panelservices WHERE panelservicesid = (SELECT MAX(panelservicesid) FROM panelservices);"
    crear_conexion()
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    return data[0]

def tiempo_apertura():
    crear_conexion()
    query = "SELECT t_apertura FROM config;"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    data = data[0]
    return data


# PENDIENTE REVISAR 
def Num_serie():
    query = "SELECT serialnumber FROM panelcat;"
    crear_conexion()
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    return data


def estado_sistema():
    crear_conexion()
    query = "SELECT no_serie_acceso, rate, t_apertura, no_venta_act, shift_no_act, no_serie_payout, no_serie_hopper from config;"
    cursor.execute(query)
    data = cursor.fetchone()
    matar_conexion()
    rate = data[0]
    return data


def cambiar_estado_sistema(numSerie, tariafa, t_apertura, num_payout, num_hopper):
    crear_conexion()
    query = "UPDATE config SET " \
            "no_serie_acceso = '"+numSerie+"', " \
            "rate = '"+tariafa+"', " \
            "t_apertura = '"+t_apertura+"', " \
            "no_serie_payout = '"+num_payout+"', " \
            "no_serie_hopper = '"+num_hopper+"';"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def canales_monedero():
    crear_conexion()
    query = "SELECT canal, estado FROM canales_hopper"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def canales_billetero():
    crear_conexion()
    query = "SELECT canal, estado FROM canales_payout"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data

#########################################################
#                                                       #
#                   MONEDERO                            #
#                                                       #
#########################################################

def cambioMonedero(m05, m1, m2, m5, m10):
    query = "UPDATE canales_hopper set estado = '"+ m05 +"' WHERE canal = 0.5;"
    query2 = "UPDATE canales_hopper set estado = '"+ m1 +"' WHERE canal = 1;"
    query3 = "UPDATE canales_hopper set estado = '"+ m2 +"' WHERE canal = 2;"
    query4 = "UPDATE canales_hopper set estado = '"+ m5 +"' WHERE canal = 5;"
    query5 = "UPDATE canales_hopper set estado = '"+ m10 +"' WHERE canal = 10;"

    queryBanderaCambio = "UPDATE config set cambio_canales_hopper = '1'"   # Indica al socket que hay un cambio en los canales

    crear_conexion()
    
    cursor.execute(query)
    db.commit()
    cursor.execute(query2)
    db.commit()
    cursor.execute(query3)
    db.commit()
    cursor.execute(query4)
    db.commit()
    cursor.execute(query5)
    db.commit()
    cursor.execute(queryBanderaCambio)
    db.commit()
    matar_conexion()


# Consulta si hay un cambio en los canales del monedero
def hayCambiosMonedero():
    crear_conexion()
    query = "SELECT cambio_canales_hopper FROM config"
    cursor.execute(query)
    data = cursor.fetchone()
    data = str(data[0])
    if data == '1':
        return True
    else:
        return False


# Desactiva la bandera del cambio en los canales
def desactivarCambioMonedero():
    crear_conexion()
    query =  "UPDATE config set cambio_canales_hopper = '0'"
    cursor.execute(query)
    db.commit()
    matar_conexion()


#########################################################
#                                                       #
#                      BILLETERO                        #
#                                                       #
#########################################################

def cambioBilletero(b20, b50, b100, b200, b500):
    query = "UPDATE canales_payout set estado = '"+ b20 +"' WHERE canal = 20;"
    query2 = "UPDATE canales_payout set estado = '"+ b50 +"' WHERE canal = 50;"
    query3 = "UPDATE canales_payout set estado = '"+ b100 +"' WHERE canal = 100;"
    query4 = "UPDATE canales_payout set estado = '"+ b200 +"' WHERE canal = 200;"
    query5 = "UPDATE canales_payout set estado = '"+ b500 +"' WHERE canal = 500;"
    crear_conexion()
    cursor.execute(query)
    db.commit()
    cursor.execute(query2)
    db.commit()
    cursor.execute(query3)
    db.commit()
    cursor.execute(query4)
    db.commit()
    cursor.execute(query5)
    db.commit()
    matar_conexion()

#########################################################
#                                                       #
#                       VENTA                           #
#                                                       #
#########################################################


def consultarTicket():
    crear_conexion()
    query = "SELECT no_venta_act FROM config"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data[0][0]

def idpanelServices():
    crear_conexion()
    query = "SELECT servicesdetailid from servicesdetail  ORDER BY servicesdetailid DESC limit 1;"
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) == 0:
        data = '0'
    else:
        data = data[0][0]
        matar_conexion()
        data = int(data) +  1
    return data


def insertar_venta(query):
    crear_conexion()
    cursor.execute(query)
    db.commit()
    matar_conexion()

#########################################################
#                                                       #
#                    BITACORA                           #
#                                                       #
#########################################################


def registro_bitacora(usuario, inicio_sesion, fin_sesion):
    crear_conexion()
    query ="INSERT INTO bitacora(username, startsesion, endsesion) VALUES('"+usuario+"'," \
                                                                              " '"+inicio_sesion+"', " \
                                                                              "'"+fin_sesion+"');"
    cursor.execute(query)
    db.commit()
    matar_conexion()


def consulta_bitacora(indice):
    crear_conexion()
    query="SELECT username, startsesion, endsesion FROM bitacora limit "+str(indice)+" , 50;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def bitacora():
    crear_conexion()
    query="SELECT username, startsesion, endsesion FROM bitacora ;"
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data


def ejecutar(query):
    crear_conexion()
    cursor.execute(query)
    data = cursor.fetchall()
    matar_conexion()
    return data
