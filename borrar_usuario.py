# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import render_template, request, redirect, session, url_for
from libgral import tabla_usuarios, paginacion
from class_db import eliminar_usuario

direccion = "borrar-usuario"
mensaje = "BorrarCuentas"


class borrarUsuario(flask.views.MethodView):
    def post(self):
        username = request.form['Busuario']
        eliminar_usuario(username)
        tablaUsuarios = tabla_usuarios(0, 'Borrar')
        indice_paginacion = paginacion(1, 0, direccion)
        return render_template('Borrar_Usuarios.html', tabla_usuarios=tablaUsuarios,
                               indice_paginacion=indice_paginacion,
                               mensaje=mensaje)

    def get(self):
        if len(session) > 1 and session['typeuser'] == 'Administrador':
            indice = str(request.args.get('indice'))
            pagina = str(request.args.get('pagina'))
            if indice == "None" and pagina == "None":
                indice = 0
                pagina = 1

            tablaUsuarios = tabla_usuarios(indice, 'Borrar')
            indice_paginacion = paginacion(pagina, indice, direccion)
            return render_template('Borrar_Usuarios.html', tabla_usuarios=tablaUsuarios,
                                   indice_paginacion=indice_paginacion)

        else:
            return redirect(url_for('login'))

