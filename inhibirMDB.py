import serial
import time
import logger
strd_0  = "  SIN SERVICIO  "
strd_1  = "                "


def main():
    try:
	for intento in range(0,2):
            serial_MDB = serial.Serial('/dev/ttyUSBMDB', 9600, timeout = 0.1)
            serial_MDB.write('\x0C\x00\x00\x00\x00')        #Inhabilitar Monedero MDB
	    rx = str(serial_MDB.readline())
            serial_MDB.close()
	    if rx == "00":
		break
    except:
        logger.error("No esta disponible el puerto ttyUSBMDB")
    time.sleep(1)
    try:
        serial_Display = serial.Serial('/dev/ttyUSBDisplay', 9600, timeout = 0.1)
        serial_Display.write('CS\x00')
        serial_Display.write('TP\x01\x00')
        serial_Display.write('TT SIN SERVICIO   ')
        serial_Display.write('\x00\x00')
        serial_Display.write('TT                ')
        #serial_MDB.write('\x0C\xFF\xFF\xFF\xFF')	# Habilitar Monedero MDB
        #time.sleep(0.50)
        serial_Display.close()
    except:
        logger.error("No esta disponible el puerto ttyUSBDisplay")


main()
