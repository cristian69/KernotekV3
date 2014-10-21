# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import logging
import logging.handlers
import os
import sys
import threading

__PATH__ = "/var/log/KERNOTEK"

__FORMAT__ = '%(asctime)s| %(lineno)4s| %(message)-s'
__DATE_FMT__ = '%y-%m-%d %H:%M:%S'

LOGFILESIZE = 31457280
MAXLOGFILES = 2


def cerradura(msg):
    if validatePath(__PATH__):
        __FORMAT__ = '%(asctime)s| %(message)-s'
        logger = logging.getLogger('/var/log/KERNOTEK/cerradura.log')
        logger.setLevel(logging.ERROR)
        handler = logging.handlers.RotatingFileHandler(filename='/var/log/KERNOTEK/cerradura.log', mode='a', maxBytes=LOGFILESIZE,
                                                       backupCount=MAXLOGFILES)
        formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(msg)
	pathCerradura = '/var/log/KERNOTEK/cerradura.log'
        hilo = threading.Thread(target=limpiarLog, name="Hilo_limpiar_log", args=( pathCerradura, ) )
        hilo.start()


def error(msg):
    if validatePath(__PATH__):
        logger = logging.getLogger('/var/log/KERNOTEK/error.log')
        logger.setLevel(logging.ERROR)
        handler = logging.handlers.RotatingFileHandler(filename='/var/log/KERNOTEK/error.log', mode='a', maxBytes=LOGFILESIZE,
                                                       backupCount=MAXLOGFILES)
        formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(msg)
	pathError = '/var/log/KERNOTEK/error.log'
        hilo = threading.Thread(target=limpiarLog, name="Hilo_limpiar_log", args= (pathError, ) )
        hilo.start()


def warning(msg):
    if validatePath(__PATH__):
        logger = logging.getLogger('/var/log/KERNOTEK/warning.log')
        logger.setLevel(logging.WARNING)
        handler = logging.handlers.RotatingFileHandler(filename='/var/log/KERNOTEK/warning.log', mode='a', maxBytes=LOGFILESIZE,
                                                       backupCount=MAXLOGFILES)
        formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(msg)
	pathWarning = '/var/log/KERNOTEK/warning.log'
        hilo = threading.Thread(target=limpiarLog, name="Hilo_limpiar_log", args= ( pathWarning, ) )
        hilo.start()


# def critical(msg):
#     if validatePath(__PATH__):
#         logger = logging.getLogger('/var/log/KERNOTEK/CRITICAL')
#         logger.setLevel(logging.CRITICAL)
#         handler = logging.handlers.RotatingFileHandler(filename='/var/log/KERNOTEK/CRITICAL', mode='a', maxBytes=LOGFILESIZE,
#                                                        backupCount=MAXLOGFILES)
#         formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#         logger.error(msg)

def debug(msg):
    if validatePath(__PATH__):
        logger = logging.getLogger('/var/log/KERNOTEK/debug.log')
	
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(filename='/var/log/KERNOTEK/debug.log', mode='a', maxBytes=LOGFILESIZE,
                                                       backupCount=MAXLOGFILES)
        formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(msg)
	pathDebug = "/var/log/KERNOTEK/debug.log"
        hilo = threading.Thread(target=limpiarLog, name="Hilo_limpiar_log", args= (pathDebug, ) )
        hilo.start()


def seguridad(msg):
    if validatePath(__PATH__):
        logger = logging.getLogger('/var/log/KERNOTEK/seguridad.log')
        logger.setLevel(logging.WARNING)
        handler = logging.handlers.RotatingFileHandler(filename='/var/log/KERNOTEK/seguridad.log', mode='a', maxBytes=LOGFILESIZE,
                                                       backupCount=MAXLOGFILES)
        formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(msg)
	pathSeguridad = '/var/log/KERNOTEK/seguridad.log'
        hilo = threading.Thread(target=limpiarLog, name="Hilo_limpiar_log", args=( pathSeguridad, ) )
        hilo.start()


def limpiarLog(ruta):
    cursor = open(ruta,'r')
    listaLog = cursor.readlines()
    cursor.close()
    cursor = open(ruta, "w")
    linea1 = ""
    for linea in listaLog:
        if linea1 != linea:
            cursor.write(linea)
        linea1 = linea
    cursor.close()


def validatePath(strpath):
    try:
        if not os.path.isdir(strpath):
            # Tratara de crearla
            os.makedirs(strpath)
        return True
    except OSError, err:
        if err.errno == 13:
            print >> sys.stderr, \
                "No se puede crear el directorio  \"%s\", revisar permisos" % (strpath)

