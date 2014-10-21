# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import render_template, redirect, url_for, session, request
from libgral import tabla_usuarios, paginacion

direccion = "usuarios"


class verUsuarios(flask.views.MethodView):
    def get(self):
        if len(session) > 1 and session['typeuser'] == 'Administrador':
            indice = str(request.args.get('indice'))
            pagina = str(request.args.get('pagina'))
            if indice == "None" and pagina == "None":
                indice = 0
                pagina = 1
            tablaUsuarios = tabla_usuarios(indice, "")
            indice_paginacion = paginacion(pagina, indice, direccion)
            return render_template('Cuentas_Usuarios.html',
                                   tabla_usuarios=tablaUsuarios,
                                   indice_paginacion=indice_paginacion)
        else:
            return redirect(url_for('login'))




