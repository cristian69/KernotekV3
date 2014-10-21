# -*- coding: utf-8 -*-

__author__ = 'aramirez'
import flask
from flask import render_template, redirect, session, url_for, request
import class_db
import logger


class configReporte(flask.views.MethodView):
    def get(self):
        if len(session) > 1:
            try:
                columnasHabilitadas = columnas()
            except:
                # Agregar el registro al log
                return redirect(url_for('login'))
            return render_template('Config_Reportes.html', columnas=columnasHabilitadas)
        else:
            return redirect(url_for('login'))

    def post(self):
        ticket = str(request.form['ticket'])
        turno = str(request.form['turno'])
        fecha = str(request.form['fecha'])
        numDetalle = '0'
        tarifa = str(request.form['tarifa'])
        total = str(request.form['total'])
        nuevoEstado = ticket + '-' + turno + '-' + fecha + '-' + numDetalle + '-' + tarifa + '-' + total
        try:
            class_db.modificar_reporte(nuevoEstado)
            columnasHabilitadas = columnas()
            return render_template('Config_Reportes.html', columnas=columnasHabilitadas)
        except:
            # Agregar la parte de registrar el error en el log
            return redirect(url_for('login'))
def columnas():
    columnasDisponibles = str(class_db.consultaColumnas())
    columnasDisponibles = columnasDisponibles.split('-')
    dicColumnas = {'ticket': columnasDisponibles[0],
                   'turno': columnasDisponibles[1],
                   'fecha': columnasDisponibles[2],
                   'tarifa': columnasDisponibles[4],
                   'total': columnasDisponibles[5]}
    return dicColumnas