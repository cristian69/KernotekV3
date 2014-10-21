# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import render_template, session, url_for, redirect, request
import class_db

class Perfil(flask.views.MethodView):
    def post(self):
        datos = {'nombre': request.form['nombre'],
                 'appaterno': request.form['appaterno'],
                 'apmaterno': request.form['apmaterno'],
                 'email': request.form['email']}
        class_db.modificarUsuario(session['username'], datos)
        perfil = datos_perfil(session['username'])
        session['fullname'] = class_db.nombre_completo_usuario(session['username'])
        return render_template('Perfil.html',
                               perfil = perfil)
    def get(self):
        if len(session) > 1:
            perfil = datos_perfil(session['username'])
            return render_template('Perfil.html',
                                   perfil =perfil)
        else:
            return redirect(url_for('login'))

def datos_perfil(username):
    datos = class_db.datos_perfil(username)
    perfil = {'nombre':datos[0],
              'appaterno':datos[1],
              'apmaterno':datos[2],
              'username':datos[3],
              'email':datos[4],
              'tipo_cuenta':datos[5]}
    return perfil