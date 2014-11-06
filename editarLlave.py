#-*- coding:utf-8  -*-
__autor__ = "aramirez"

import flask
from flask import render_template, redirect, session, request, url_for
import class_db
from libgral import generar_tabla, paginacion

class EditarLlave(flask.views.MethodView):
    def get(self):
        if len(session) > 1 and session['typeuser'] == "Administrador":
            indice = str(request.args.get('indice'))
            pagina = str(request.args.get('pagina'))
            if indice == "None" and pagina == "None":
                indice = 0
                pagina = 1
            tablaLlaves = llaves(indice)
            indice_paginacion = paginacion(pagina, indice, "editar-llave")
            return render_template('llavesEditar.html',
                                   tablaLlaves=tablaLlaves,
                                   indice_paginacion=indice_paginacion)
        else:
            return redirect(url_for('login'))

    def post(self):
        bandera = request.form['submit']
        if bandera == "aceptarCambio":
            nombre = request.form['nombre']
            apPaterno = request.form['apPaterno']
            apMaterno = request.form['apMaterno']
            grupo = request.form['grupo']
            tipoLlave = request.form.getlist('tipoLlave')
            llave = request.form['llave']
            estado = request.form.getlist('estadoLlave')
            class_db.editarLlave(nombre, apPaterno, apMaterno, grupo, tipoLlave[0], llave.upper(), estado[0])
            indice = str(request.args.get('indice'))
            pagina = str(request.args.get('pagina'))
            if indice == "None" and pagina == "None":
                indice = 0
                pagina = 1
            tablaLlaves = llaves(indice)
            indice_paginacion = paginacion(pagina, indice, "editar-llave")
            return render_template('llavesEditar.html',
                                   tablaLlaves=tablaLlaves,
                                   indice_paginacion=indice_paginacion,
                                   bandera="cambioCorecto")
        if bandera == "borrarLlave":
            numLlave = request.form['codigoLlave']
            class_db.eliminarLlave(numLlave)
            indice = str(request.args.get('indice'))
            pagina = str(request.args.get('pagina'))
            if indice == "None" and pagina == "None":
                indice = 0
                pagina = 1
            tablaLlaves = llaves(indice)
            indice_paginacion = paginacion(pagina, indice, "editar-llave")
            return render_template('llavesEditar.html',
                                   tablaLlaves=tablaLlaves,
                                   indice_paginacion=indice_paginacion,
                                   bandera="borradoLlave")


def llaves(indice):
    datos = class_db.consultarLlaves(indice)
    if len(datos) == 0:
        return ""
    else: 
        tablaLlaves = generar_tabla(datos, "", "")
        return tablaLlaves