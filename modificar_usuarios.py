# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import render_template, redirect, session, url_for
from libgral import tabla_usuarios


class modificarUsuario(flask.views.MethodView):
    def post(self):
        pass
    def get(self):
        if len(session) > 1 and session['typeuser'] == 'Administrador':
            tablaUsuarios = tabla_usuarios()
            return render_template('Modificar_Usuario.html',
                                   tabla_usuarios = tablaUsuarios)
        else:
            return redirect(url_for('login'))


