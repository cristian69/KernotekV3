#-*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import redirect, request, url_for
import class_db

class RegistroUsuario(flask.views.MethodView):
    def post(self):
        nombre = request.form['nombre']
        appaterno = request.form['appaterno']
        appmaterno = request.form['apmaterno']
        email = request.form['email']
        tipo_usuario = request.form.getlist('tipo_cuenta')
        username = request.form['username']
        password = request.form['password']

        if class_db.validar_username(username):
            class_db.nuevo_usuario(nombre, appaterno, appmaterno, username, password, email, tipo_usuario[0])
            return flask.render_template('login.html', bandera="RegistroExitoso")
        else:
            return flask.render_template('login.html', bandera="RegistroError")