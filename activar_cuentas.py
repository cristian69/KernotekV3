# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import render_template, redirect, session, request, url_for
from libgral import generar_tabla, paginacion
from class_db import ver_usuarios_inactivos
import class_db

__ADDRESS__ = "activar-cuentas"  # Indica a donde la dirrecion de la paginacion
__MSG__ = "ActivarCuentas"       # Bandera para el control de los mensajes en la vista


class activarCuentas(flask.views.MethodView):
    def post(self):
        username = request.form['Ausuario']
        class_db.activarCuenta(username)
        tabla_usuario = ver_usuarios(0)
        indice_paginacion = paginacion(1, 0, __ADDRESS__)
        return render_template('Activar_Cuentas.html', tabla_usuarios=tabla_usuario,
                               indice_paginacion=indice_paginacion,
                               mensaje=__MSG__)

    def get(self):
        if len(session) > 1 and session['typeuser'] == 'Administrador':
            indice = str(request.args.get('indice'))
            pagina = str(request.args.get('pagina'))
            if indice == "None" and pagina == "None":
                indice = 0
                pagina = 1
            tabla_usuario = ver_usuarios(indice)
            indice_paginacion = paginacion(pagina, indice, __ADDRESS__)
            return render_template('Activar_Cuentas.html',
                                   tabla_usuarios=tabla_usuario,
                                   indice_paginacion=indice_paginacion)
        else:
            return redirect(url_for('login'))


def ver_usuarios(indice):
    datos = ver_usuarios_inactivos(indice)
    tabla_usuarios = generar_tabla(datos, 'ActivarUsuario', True)
    return tabla_usuarios