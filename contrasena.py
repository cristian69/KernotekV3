# -*- coding: utf-8 -*-
__author__ = 'aramirez'
import flask
from flask import render_template, request, redirect, url_for, session
import class_db
from perfil import datos_perfil


class cambiarPassword(flask.views.MethodView):
    def get(self):
        perfil = datos_perfil(session['username'])
        if len(session) > 1:
            return render_template('Perfil.html', perfil=perfil)
        else:
            return redirect(url_for('login'))

    def post(self):
        passwordIngresado = request.form['passwordActual']
        nuevoPassword = request.form['nuevoPassword']
        passwordConsultado = class_db.consultarPassword(session['username'])
        perfil = datos_perfil(session['username'])
        if passwordIngresado == passwordConsultado:
            class_db.restablecer_password(session['username'], nuevoPassword)
            return render_template('Perfil.html', perfil=perfil, bandera="passwordValido")
        else:
            return render_template('Perfil.html', perfil=perfil, bandera="passwordInvalido")

