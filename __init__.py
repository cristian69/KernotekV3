# -*- coding:utf-8 -*-

"""
    DEPENDENCIAS

    * Instalar pip con el archivo get-pip.py
    * pip install flask
    * sudo apt-get install python-mysqldb
    * pip install flask-mysql
    * pip install xlsxwriter
    * apt-get install python-dev build-essential
    * pip install xhtml2pdf
    * apt-get install uwsgi-plugin-python    
    * apt-get install uwsgi
    * apt-get install nginx
    * apt-get isntall mariadb-server
    * apt-get install procname
    NUEVA LIBRERIA PARA EXPORTAR A PDF
    
    * urpmi libffi-devel   - mageia
    * apt-get install libffi-dev - Ubuntu
    * apt-get install python-lxml
    * pip install WeasyPrint
    * pip install pango
   

    CODIFICACION

    Para corregir el error de la codificacción 
    * http://rm-rf.es/python-cambiar-codificacion-encoding-por-defecto/


"""

import flask
from flask import render_template, session
from datetime import datetime
import classdb
import shutil

#------------vistas
from login import Login
import os

from home import Home
from logout import Logout
from reportegeneral import reporteGeneral
from reporteespecifico import reporteEspecifico
from reportedetallado import reporteDetallado
from reporteturno import reporteTurno
from corteturno import corteTurno

from reportes import Reportes
from turnos import Turnos
from configuracionsistema import Configuracion

app = flask.Flask(__name__)
######### Inicializacion del servidor ####################
__SERVER__ = '0.0.0.0'
__PORT__ = 5000
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
        classdb.registro_bitacora(session['username'], session['startsession'], session['endsession'])
        shutil.rmtree("/var/www/kernotekv3/static/download/"+session['username'])
        session.clear()

        return flask.render_template('cerrarSesion.html')
    
    else:
        session.clear()
    return flask.redirect(flask.url_for('login'))

app.add_url_rule('/login/', view_func=Login.as_view('login'), methods=['POST', 'GET'])
app.add_url_rule('/home/', view_func=Home.as_view('home'), methods=['POST', 'GET'])
app.add_url_rule('/reportes/', view_func=Reportes.as_view('reportes'), methods=['POST', 'GET'])
app.add_url_rule('/turnos/', view_func=Turnos.as_view('turnos'), methods=['GET', 'POST'])
app.add_url_rule('/configuracion/', view_func=Configuracion.as_view('configuracion'), methods=['GET', 'POST'])
app.add_url_rule('/reporte-turno/', view_func=reporteTurno.as_view('reporteTurno'), methods=['GET', 'POST'])


#app.add_url_rule('/logout/', view_func=Logout.as_view('logout'), methods=['POST'])
app.add_url_rule('/reporte-general/', view_func=reporteGeneral.as_view('reporteGeneral'), methods=['POST', 'GET'])
app.add_url_rule('/reporte-especifico/', view_func=reporteEspecifico.as_view('reporteEspecifico'), methods=['GET', 'POST'])
app.add_url_rule('/reporte-detallado', view_func=reporteDetallado.as_view('reporteDetallado'), methods=['GET', 'POST'])
app.add_url_rule('/corte-turno/', view_func=corteTurno.as_view('corteTurno'), methods=['POST', 'GET'])

########## Inicializacion del servidor ##############################
if __name__ == '__main__':
    app.run(host=__SERVER__, port=__PORT__)

####################################################################

