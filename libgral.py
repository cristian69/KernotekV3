# -*- coding:utf-8 -*-
import datetime
import class_db
from datetime import date
from flask import session
import os
import signal
import time


registros_pagina = 50 # El número de registros tiene que ser multiplo de la variable de clase db en la consulta

def terminarProceso():
    for proceso in os.popen("ps xa"):
        proceso = proceso.split()
        for valor in proceso:
            valor = valor.split('/')
            for valor2 in valor:
                if valor2 == "BasicValidator" or valor2 == "servidor.py":
                    pid = int(proceso[0])
                    try:
                        os.kill(pid, signal.SIGKILL)
                    except:
                        print "No se pude terminar el proceso"


def iniciarProceso():
    START = "service appserver start"
    try:
        os.system(START)

    except:
        print "No se puede iniciar"


def reiniciarProceso():
    terminarProceso()
    time.sleep(1)
    iniciarProceso()

def revisarProceso():
    socketPython = False
    socketC = False
    for vuelta in range(0,1):
        for proceso in os.popen("ps xa"):
            proceso = proceso.split()
            for valor in proceso:
                valor = valor.split('/')
                for valor2 in valor:
                    if valor2 == "BasicValidator":
                        socketC = True
                    if valor2 == "servidor.py":
                        socketPython = True
    return socketC, socketPython


def generarProximoCorte(tiempo1):
    valoresTiempo1 = tiempo1.split(':')
    horas1 = valoresTiempo1[0]
    minutos1 = valoresTiempo1[1]
    segundos1 = valoresTiempo1[2]

    tiempo2 = str(ObtenerHora())

    valoresTiempo2 = tiempo2.split(':')
    horas2 = valoresTiempo2[0]
    minutos2 = valoresTiempo2[1]
    segundos2 = valoresTiempo2[2]
    
    totalHoras = int(horas1) + int(horas2)
    totalMinutos = int(minutos1) + int(minutos2)
    totalSegundos = int(segundos1) + int(segundos2)
    proxCorte = calcularTiempo(totalHoras, totalMinutos, totalSegundos)
    
    return proxCorte



def calcularTiempo(totalHoras, totalMinutos, totalSegundos):
    agregadoMinutos = 0
    agregadoHoras = 0

    while totalSegundos >= 60:
        agregadoMinutos +=1
        totalSegundos -= 60

    
    if totalSegundos < 10:
        totalSegundos = '0' + str(totalSegundos) 

    totalMinutos += agregadoMinutos

    while totalMinutos >= 60:
        agregadoHoras +=1
        totalMinutos -= 60


    if totalMinutos < 10:
        totalMinutos = '0' + str(totalMinutos)

    totalHoras += agregadoHoras
    
    if totalHoras > 24:
        totalHoras -= 24

    tiempo = str(totalHoras) +":"+ str(totalMinutos) + ":" + str(totalSegundos)
    
    return tiempo



def nombreDias(dia):
    if dia == "Monday":
        return "Lunes"
    elif dia == "Tuesday":
        return "Martes"
    elif dia == "Wednesday":
        return "Miercoles"
    elif dia == "Thursday":
        return "Jueves"
    elif dia == "Friday":
        return "Viernes"
    elif dia == "Saturday":
        return "Sabado"
    elif dia == "Sunday":
        return "Domingo"

# Pendiente modificar para adaptarlo a la clase servidor

def obtenerNombreDia():
    dia = datetime.datetime.now()
    dia = dia.strftime("%A")
    if dia == "Monday":
        return "Lunes"
    elif dia == "Tuesday":
        return "Martes"
    elif dia == "Wednesday":
        return "Miercoles"
    elif dia == "Thursday":
        return "Jueves"
    elif dia == "Friday":
        return "Viernes"
    elif dia == "Saturday":
        return "Sabado"
    elif dia == "Sunday":
        return "Domingo"

def nombreMes(mes):
    if mes == "Jan":
        return "Enero"
    elif mes == "Feb":
        return "Febrero"
    elif mes == "Mar":
        return "Marzo"
    elif mes == "Apr":
        return "Abril"
    elif mes == "May":
        return "Mayo"
    elif mes == "Jun":
        return "Junio"
    elif mes == "Jul":
        return "Julio"
    elif mes == "Aug":
        return "Agosto"
    elif mes == "Sep":
        return "Septiembre"
    elif mes == "Oct":
        return "Octubre"
    elif mes == "Nov":
        return "Noviembre"
    elif mes == "Dec":
        return "Diciembre"


def obtenerDia():
    dia = datetime.datetime.now()
    dia = dia.strftime("%d")
    dia = str(dia)
    return dia

def ObtenerFecha():
    fecha = str(datetime.date.today())
    return fecha


def ObtenerHora():
    hora = str(datetime.datetime.now())
    hora = hora.split(' ') 
    hora = hora[1]  
    hora = hora.split('.')
    hora = hora[0]
    return hora


def FechaHora():
    fecha_hora = str(datetime.datetime.today())
    fecha_hora = fecha_hora.split('.')  # Separa las decimas de segundos
    fecha_hora = fecha_hora[0]  
    return fecha_hora


def generar_tabla(datos, modal, bandera):
    columnas = str(class_db.consultaColumnas()).split('-')
    bandera_tarifa = False
    bandera_deposito = False
    switch = True

    if columnas[5] == '1':
        bandera_deposito = True
    if columnas[4] == '1':
        bandera_tarifa =  True

    bandera_activa = bandera   # Sirve para camabiar a activa o desactiva las cuentas y que no afecte a los reportes
    bandera_color = True
    codigo_tabla = ""
    bandera_td = True
    id_fila = 0
    if datos is None:
        msg = False
        return msg
    else:
        for fila_datos in datos:
            id_fila = id_fila+1
            bandera_td = True
            bandera_tocket = True
            if bandera_color:
                codigo_tabla += str('<tr id="'+str(id_fila)+'" class="'+str(id_fila)+'">')
                bandera_color = False
            else:
                codigo_tabla += str('<tr id= "'+str(id_fila)+'" class="'+str(id_fila)+'">')
                bandera_color = True
            for dato in fila_datos:
		
                if bandera_activa:
                    if dato == 1:
                            dato = "Activa"
                    if dato == 0:
                            dato = "Desactiva"
		if dato == 0:
		    dato = "Cortesía"

                if bandera_td:
                    if modal is "":
                        codigo_tabla += str('<td id="key" class="'+str(id_fila)+'">') + str(dato) + str("</td>")
                    else:
                        codigo_tabla += str('<td id="key" class="'+str(id_fila)+'">') + str(dato) + str('</a>') + str("</td>")
                    bandera_td = False
                else:
                    codigo_tabla += str("<td>") + str(dato) + str("</td>")
            codigo_tabla += str("</tr>")
    return codigo_tabla


def tabla_usuarios(indice, modal):
    bandera = True                  # Indica que si se quiere cambiar el 0 por inactiva o 1 por activa
    datos = class_db.ver_usuarios(indice)
    tabla = generar_tabla(datos, modal, bandera)
    return tabla


def numeracion_paginas(fecha_inicio, fecha_fin, pag_activa, indice, direccion):  # REGRESA EL CÓDIGO HTML DE LA PAGINACIÓN
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
                    '&num_pagina=' + str(nextBlock) +'">'\
                    '<i class="fa fa-angle-double-right"></i></a></li>')
    return codeIndex




def paginacion(pag_activa, indice, direccion):  # REGRESA EL CÓDIGO HTML DE LA PAGINACIÓN
    indice_next = int(indice) + registros_pagina
    indice_back = int(indice) - registros_pagina

    if direccion == "bitacora":
        total_registro = class_db.bitacora()
    elif direccion == "usuarios" or direccion == "borrar-usuario":
        total_registro = class_db.totalUsuarios()
    elif direccion == "activar-cuentas":
        total_registro = class_db.usuarioInacticvos()
    elif direccion == "editar-llave":
        total_registro = class_db.totalLlaves()
    count = 0
    num_pagina = 1
    if int(pag_activa) != 1:
        back_pag = int(pag_activa) - 1
        codigo_pag = str('<li class="enable"><a href="/'+direccion+'/?'
                         'indice=' + str(indice_back) + ''
                         '&pagina=' + str(back_pag) + '"><strong>&laquo;</strong></a></li>')
    else:
        codigo_pag = str('<li class="disabled"><a href="#">&laquo;</a></li>')
    if int(pag_activa) == 1:
        codigo_pag += str('<li class="active" id = "pag' + str(num_pagina) + '">')
    else:
        codigo_pag += str('<li id = "pag' + str(num_pagina) + '">')

    codigo_pag += str('<a href="/'+direccion+'/?'
                      'indice=0'
                      '&pagina=' + str(num_pagina) + '">1<span class="sr-only">(current)</span></a></li>')

    total_registro = len(total_registro)
    indice = 0

    for num in range(0, total_registro):
        if count == registros_pagina:
            indice += registros_pagina
            num_pagina += 1

            if int(num_pagina) == int(pag_activa):
                codigo_pag += str('<li class="active" id = "pag' + str(num_pagina) + '">')
            else:
                codigo_pag += str('<li id = "pag' + str(num_pagina) + '">')

            codigo_pag += str('<a href="/'+direccion+'/?'
                              'indice=' + str(indice) + ''
                              '&pagina=' + str(num_pagina) + '">' + str(num_pagina) + '<span class="sr-only">(current)</span></a></li>')
            count = 0
        count += 1

    if int(pag_activa) != num_pagina:
        next_pag = int(pag_activa) + 1
        codigo_pag += str('<li class="enable"><a href="/'+direccion+'/?'
                          'indice=' + str(indice_next) + ''
                          '&pagina=' + str(next_pag) + '">&raquo;</a></li>')
    else:
        codigo_pag += str('<li class="disabled"><a href="#">&raquo;</a></li>')

    return codigo_pag

# if __name__ == "__main__":
#     print ObtenerFecha()
#     print ObtnerHora()
#     print FechaHora()
#     print obtenerNombreDia()
#     print obtenerDia()
