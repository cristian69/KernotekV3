# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import render_template, redirect, url_for, session, request
from libgral import generar_tabla, paginacion
import class_db

class Bitacora(flask.views.MethodView):
    def get(self):
        if len(session) > 1 and session['typeuser'] == "Administrador":
            indice = str(request.args.get('indice'))
            pagina = str(request.args.get('pagina'))
            if indice == "None" and pagina == "None":
                indice = 0
                pagina = 1
            tabla_bitacora = datos_bitacora(indice)
            indice_paginacion = paginacion(pagina, indice, "bitacora")
            return render_template('Bitacora.html',
                                   tabla_bitacora = tabla_bitacora,
                                   indice_paginacion = indice_paginacion)
        else:
            return redirect(url_for('login'))


def datos_bitacora(indice):
    datos = class_db.consulta_bitacora(indice)
    tabla_bitacora = generar_tabla(datos, "", "")
    return tabla_bitacora