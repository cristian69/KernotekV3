import flask.views
from flask import request, session
from flaskext.mysql import MySQL

import flask
import class_db
import datetime
import os


mysql = MySQL()
app = flask.Flask(__name__)


class Login(flask.views.MethodView):
    def post(self):
        session.clear()
        message = None
        if request.method == 'POST':
            usuario = request.form['username']
            password = request.form['password']
            data = class_db.validar_usuario(usuario, password)
            if data is None:
                session.clear()
                return flask.render_template('login.html', bandera="UsuarioInvalido")
            else:
                typeuser = data[1]
                session['username'] = usuario
                session['typeuser'] = typeuser
                session['startsession'] = str(datetime.datetime.today())
                session['fullname'] = class_db.nombre_completo_usuario(usuario)
                carpetaPersonal = "/var/www/kernotekv3/static/download/"+session['username']+"/"
                if not os.path.exists(carpetaPersonal):
                    os.makedirs(carpetaPersonal)
                return flask.redirect(flask.url_for('home'))
        else:
            session.clear()
            return redirect(url_for('login'))

    def get(self):
        session.clear()
        return flask.render_template('login.html', message='Access denied')
