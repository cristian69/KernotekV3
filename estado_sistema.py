# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import flask
from flask import session, redirect, render_template, url_for
import class_db


class estadoSistema(flask.views.MethodView):
    def get(self):
        if len(session) > 1:
            datos_sistema = sistema()
            estado_monedero = monedero()
            estado_billetero = billetero()
            return render_template('Estado_Sistema.html',
                                   datos_sistema = datos_sistema,
                                   estado_monedero = estado_monedero,
                                   estado_billetero = estado_billetero)
        else:
            return redirect(url_for('login'))



def sistema():
    data = class_db.estado_sistema()
    datos_sistema = {'numSerie': '',
                    'rate':'',
                    't_apertura':'',
                    'ticket_actual':0,
                    'turno':0,
                    'num_payout':'',
                    'num_hopper':''}

    datos_sistema['numSerie'] = data[0]
    datos_sistema['rate'] =str(data[1]) + "0"
    datos_sistema['t_apertura'] = str(data[2])
    datos_sistema['ticket_actual'] = data[3]
    datos_sistema['turno'] = data[4]
    datos_sistema['num_payout'] = data[5]
    datos_sistema['num_hopper'] = data[6]
    return datos_sistema


def monedero():
    estado_monedero = {0.5:'',
                       1.0:'',
                       2.0:'',
                       5.0:'',
                       10.0:''}

    canales_estados = class_db.canales_monedero()
    for canales in canales_estados:
        estado_monedero[canales[0]] = canales[1]

    return estado_monedero


def billetero():
    estado_billetero = {20:'',
                        50:'',
                        100:'',
                        200:'',
                        500:''}

    canales_estados = class_db.canales_billetero()
    for canales in canales_estados:
        estado_billetero[canales[0]] = canales[1]

    return estado_billetero
