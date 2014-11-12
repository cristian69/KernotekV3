# -*- coding:utf-8 -*-

"""
    DEPENDENCIAS

    * Instalar pip con el archivo get-pip.py
    * pip install flask
    * sudo apt-get install python-mysqldb
    * pip install flask-mysql
    * pip install xlsxwriter
    * apt-get install python-dev
    * pip install xhtml2pdf
    * pip install python-flup
    

    NUEVA LIBRERIA PARA EXPORTAR A PDF
    
    * urpmi libffi-devel   - mageia
    * apt-get install libffi-dev - Ubuntu
    * apt-get install python-lxml
    * pip install WeasyPrint

    CODIFICACION

    Para corregir el error de la codificacción 
    * http://rm-rf.es/python-cambiar-codificacion-encoding-por-defecto/


"""

import flask
from flask import render_template, session
from datetime import datetime
import class_db
import shutil

#------------vistas
from class_login import Login
import os
from contrasena import cambiarPassword

from home import Home
from logout import Logout
from ver_usuarios import verUsuarios
from registro_usuario import RegistroUsuario
from borrar_usuario import borrarUsuario
from activar_cuentas import activarCuentas
from reporte_general import reporteGeneral
from estado_sistema import estadoSistema
from reporte_especifico import reporteEspecifico
from bitacora import Bitacora
from perfil import Perfil
from config_sistema import ConfigSistema
from configReporte import configReporte
from reporteDetallado import reporteDetallado
from reporteTurno import reporteTurno
from corteTurno import corteTurno
from nuevaLlave import NuevaLlave
from editarLlave import EditarLlave

from reportes import Reportes

app = flask.Flask(__name__)
######### Inicializacion del servidor ####################
__SERVER__ = '0.0.0.0'
__PORT__ = 8000
app.debug = True

#fin de los parametros para la inicializacion del servidor
app.secret_key = os.urandom(24)


@app.route('/')
def infoServer():
    return render_template('login.html')



@app.route('/logout/')
def logout():
    if len(session) > 1:
        session['endsession'] = str(datetime.today())
        class_db.registro_bitacora(session['username'], session['startsession'], session['endsession'])
        shutil.rmtree("/var/www/demoFlask/static/download/"+session['username'])
        session.clear()

        return flask.render_template('cerrarSesion.html')
    
    else:
        session.clear()
    return flask.redirect(flask.url_for('login'))

app.add_url_rule('/login/', view_func=Login.as_view('login'), methods=['POST', 'GET'])
app.add_url_rule('/home/', view_func=Home.as_view('home'), methods=['POST', 'GET'])
app.add_url_rule('/reportes/', view_func=Reportes.as_view('reportes'), methods=['POST', 'GET'])

#app.add_url_rule('/logout/', view_func=Logout.as_view('logout'), methods=['POST'])
app.add_url_rule('/usuarios/', view_func=verUsuarios.as_view('verUsuarios'), methods=['GET'])
app.add_url_rule('/registro-Usuario/', view_func=RegistroUsuario.as_view('registroUsuario'), methods=['POST'])
app.add_url_rule('/borrar-usuario/', view_func=borrarUsuario.as_view('borrarUsuario'), methods=['POST', 'GET'])
app.add_url_rule('/activar-cuentas/', view_func=activarCuentas.as_view('activarCuentas'), methods=['POST', 'GET'])
app.add_url_rule('/reporte-general/', view_func=reporteGeneral.as_view('reporteGeneral'), methods=['POST', 'GET'])
app.add_url_rule('/reporte-especifico/', view_func=reporteEspecifico.as_view('reporteEspecifico'), methods=['GET', 'POST'])
app.add_url_rule('/reporte-detallado', view_func=reporteDetallado.as_view('reporteDetallado'), methods=['GET', 'POST'])
app.add_url_rule('/reporte-turno/', view_func=reporteTurno.as_view('reporteTurno'), methods=['GET', 'POST'])
app.add_url_rule('/estado-sistema/', view_func=estadoSistema.as_view('estadoSistema'), methods=['GET'])
app.add_url_rule('/bitacora/', view_func=Bitacora.as_view('bitacora'), methods=['GET'])
app.add_url_rule('/perfil/', view_func=Perfil.as_view('perfil'), methods=['GET', 'POST'])
app.add_url_rule('/config-sistema/', view_func=ConfigSistema.as_view('configSistema'), methods=['GET', 'POST'])
app.add_url_rule('/config-reporte/', view_func=configReporte.as_view('configReporte'), methods=['GET', 'POST'])
app.add_url_rule('/contrasena/', view_func=cambiarPassword.as_view('contrasena'), methods=['POST', 'GET'])
app.add_url_rule('/corte-turno/', view_func=corteTurno.as_view('corteTurno'), methods=['POST', 'GET'])
app.add_url_rule('/nueva-llave/', view_func=NuevaLlave.as_view('nuevaLlave'), methods=['POST', 'GET'])
app.add_url_rule('/editar-llave/', view_func=EditarLlave.as_view('editarLlave'), methods=['POST', 'GET'])


########## Inicializacion del servidor ##############################
if __name__ == '__main__':
    app.run(host=__SERVER__, port=__PORT__)

####################################################################

