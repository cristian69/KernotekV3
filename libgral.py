# -*- coding:utf-8 -*-
import datetime
import class_db
from datetime import date


registros_pagina = 50 # El número de registros tiene que ser multiplo de la variable de clase db en la consulta


def generarProximoCorte(tiempo1):
    valoresTiempo1 = tiempo1.split(':')
    horas1 = valoresTiempo1[0]
    minutos1 = valoresTiempo1[1]
    segundos1 = valoresTiempo1[2]

    tiempo2 = str(ObtnerHora())

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


def obtenerNombreDia():
    dia = datetime.datetime.now()
    dia = dia.strftime("%A")
    if dia == "Moday":
        dia = "Lunes"
    elif dia == "Tusday":
        dia = "Martes"
    elif dia == "Wednesday":
        dia = "Miercoles"
    elif dia == "Thursday":
        dia = "Jueves"
    elif dia == "Friday":
        dia = "Viernes"
    elif dia == "Saturday":
        dia = "Sabado"
    elif dia == "Sunday":
        dia == "Domingo"
    else:
        return False
    return dia


def obtenerDia():
    dia = datetime.datetime.now()
    dia = dia.strftime("%d")
    dia = str(dia)
    return dia

def ObtnerFecha():
    fecha = str(datetime.date.today())
    return fecha


def ObtnerHora():
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
    bandera_activa = bandera   # Sirve para camabiar a activa o desactiva las cuentas y que no afecte a los reportes
    bandera_color = True
    codigo_tabla = ""
    bandera_td = True
    id_fila=0
    if datos is None:
        msg = False
        return msg
    else:
        for fila_datos in datos:
            id_fila = id_fila+1
            bandera_td = True
            if bandera_color:
                codigo_tabla += str('<tr style="border-top:1px solid #eee; border-bottom:1px solid #eee;" id="'+str(id_fila)+'" class="'+str(id_fila)+'">')
                bandera_color = False
            else:
                codigo_tabla += str('<tr style="border-top:1px solid #eee; border-bottom:1px solid #eee;" id= "'+str(id_fila)+'" class="'+str(id_fila)+'">')
                bandera_color = True
            for dato in fila_datos:

                if bandera_activa:
                    if dato == 1:
                            dato = "Activa"
                    if dato == 0:
                            dato = "Desactiva"
                if dato == 0:
                    dato = "Token" # Pendiente revisar
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
    codigo_pag = ""
    indice_next = int(indice) + registros_pagina
    indice_back = int(indice) - registros_pagina
    total_registro = class_db.total_registros(fecha_inicio, fecha_fin)
    count = 0
    num_pagina = 1
    codigo_pag += str("""
                        <article class="text-right">
              <ul class="pagination">
                      """)
    if int(pag_activa) != 1:
        back_pag = int(pag_activa) - 1
        codigo_pag += str('<li class="enable"><a href="/'+direccion+'/?'
                         'indice=' + str(indice_back) + ''
                         '&fecha1=' + fecha_inicio + ''
                         '&fecha=' + fecha_fin + ''
                         '&num_pagina=' + str(back_pag) + '"><strong>&laquo;</strong></a></li>')
    else:
        codigo_pag += str('<li class="disabled"><a href="#">&laquo;</a></li>')
    if int(pag_activa) == 1:
        codigo_pag += str('<li class="active" id = "pag' + str(num_pagina) + '">')
    else:
        codigo_pag += str('<li id = "pag' + str(num_pagina) + '">')

    codigo_pag += str('<a href="/'+direccion+'/?'
                      'indice=0'
                      '&fecha1=' + fecha_inicio + ''
                      '&fecha2=' + fecha_fin + ''
                      '&num_pagina=' + str(num_pagina) + '">1<span class="sr-only">(current)</span></a></li>')

    total_registro = total_registro[0][0]
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
                              '&fecha1=' + fecha_inicio + ''
                              '&fecha2=' + fecha_fin + ''
                              '&num_pagina=' + str(num_pagina) + '">' + str(num_pagina) + '<span class="sr-only">(current)</span></a></li>')
            count = 0
        count += 1

    if int(pag_activa) != num_pagina:
        next_pag = int(pag_activa) + 1
        codigo_pag += str('<li class="enable"><a href="/'+direccion+'/?'
                          'indice=' + str(indice_next) + ''
                          '&fecha1=' + fecha_inicio + ''
                          '&fecha2=' + fecha_fin + ''
                          '&num_pagina=' + str(next_pag) + '">&raquo;</a></li>')
    else:
        codigo_pag += str('<li class="disabled"><a href="#">&raquo;</a></li>')

    codigo_pag += str('</ul></article></div>') # Fin del article y la lista
    return codigo_pag


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
#     print ObtnerFecha()
#     print ObtnerHora()
#     print FechaHora()
#     print obtenerNombreDia()
#     print obtenerDia()