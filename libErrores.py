# -*- coding: utf-8 -*-
import logger
import sms
import libgral


def registroError(msgError):
    msgError = msgError.split('|')
    msgError = msgError[1]
    if msgError.startswith('0x00'):
        return
    elif msgError == "0x0100":
        logger.debug('powering up')
        return
    elif msgError == "Initializing system.":
        logger.debug('initializing system')
        fecha = libgral.FechaHora()
        texto = str(fecha) + "hrs. " + "Inicializando sistema."
        sms.MSG(texto)
        return
    elif msgError == "0x0200":
        logger.debug("powering down")
        return
    elif msgError == "0x0300":
        logger.error("OK")
        return
    elif msgError == "0x0400":
        logger.error("keypad shifted")
        return
    elif msgError == "0x0510":
        logger.error("manual Fill / Payout active")
        return
    elif msgError == "0x0520":
        logger.error("new Inventory Information Aviable")
        return
    elif msgError == "0x0600":
        logger.error("inhibited by VMC")
        return
    elif msgError == "0x1000":
        logger.error("non especific error")
        return
    elif msgError == "0x1001":
        logger.error("data range of configuration field detected")
        return
    elif msgError == "0x1002":
        logger.error("a check sum error over a secondary data range orconfiguration field detected.")
        return
    elif msgError == "0x1003":
        logger.error("low line voltage detected")
        return
    elif msgError == "0x1100":
        logger.error("non specific discriminator error")
        return
    elif msgError == "0x1110":
        logger.error("flight deck open")
        fecha = libgral.FechaHora()
        texto = str(fecha) + "hrs. " + "Palanca de rechazo accionada."
        #sms.MSG(texto)
        return
    elif msgError == "0x1111":
        logger.error("escrow Return stuck open")
        return
    elif msgError == "0x1130":
        logger.error("coin jam in sensor")
        fecha = libgral.FechaHora()
        texto = str(fecha) + "hrs. " + "Moneda atascada en sensor."
        #sms.MSG(texto)
        return
    elif msgError == "0x1141":
        logger.error("discriminator below specified standard")
        return
    elif msgError == "0x1150":
        logger.error("validation sensor A out of range. The acceptor detects a problem with sensor A")
        return
    elif msgError == "0x1151":
        logger.error("validation sensor B out of range. The acceptor detects a problem with sensor B")
        return
    elif msgError == "0x1152":
        logger.error("validation sensor C out of range. The acceptor detects a problem with sensor C")
        return
    elif msgError == "0x1153":
        logger.error(
        'operating temperature exceeded. The acceptor detects the ambient temperature has exceeded the changer\'s operating range, thus possibly affecting the acceptance rate')
        return
    elif msgError == "0x1154":
        logger.error("sizing optics failure. The acceptor detects an error in the sizing optics")
        return
    elif msgError == "0x1200":
        logger.error("non specific accept gate error")
        return
    elif msgError == "0x1230":
        logger.error("coins entered gate, but did not exit")
        fecha = libgral.FechaHora()
        texto = str(fecha) + "hrs. " + "Moneda atorada dentro de monedero."
        #sms.MSG(texto)
        return
    elif msgError == "0x1231":
        logger.error("accept gate alarm active")
        return
    elif msgError == "0x1240":
        logger.error("accept gate open, but no coin detected")
        return
    elif msgError == "0x1250":
        logger.error("post gate sensor covered before gate opened")
        return
    elif msgError == "0x1300":
        logger.error("non specific separator error")
        return
    elif msgError == "0x1310":
        logger.error("sort sensor error. The acceptor detects an error in the sorting sensor")
        return
    elif msgError == "0x1400":
        logger.error("non specific dispenser error")
        return
    elif msgError == "0x1500":
        logger.error("non specific cassette error")
        return
    elif msgError == "0x1502":
        logger.error("cassette removed")
        fecha = libgral.FechaHora()
        texto = str(fecha) + "hrs. " + "Cassette removido."
        #sms.MSG(texto)
        return
    elif msgError == "0x1503":
        logger.error("cash box sensor error. The changer detects an error in a cash box sensor")
        return
    elif msgError == "0x1504":
        logger.error("sunlight on tube sensors. The changer detects too much ambient light on one or more of the tube sensors")
        return
    elif msgError == "0x0802":  
    	# logger.error("Changer Payout Busy")
        return
    else:
        logger.error(msgError)
        return
