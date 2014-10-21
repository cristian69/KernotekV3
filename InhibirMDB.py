import serial
import time

strd_0  = "  SIN SERVICIO  "
strd_1  = "                "


def main():
	serial_MDB = serial.Serial('/dev/ttyUSBMDB', 9600, timeout = 0.1)
        serial_Display = serial.Serial('/dev/ttyUSBPrinter', 9600, timeout = 0.1)

	#serial_MDB.open()

        serial_MDB.write('\x0C\x00\x00\x00\x00')	#Inhabilitar Monedero MDB
        serial_Display.write('CS\x00')
        serial_Display.write('TP\x01\x00')
	serial_Display.write('TT SIN SERVICIO   ')

        serial_Display.write('\x00\x00')
        serial_Display.write('TT                ')

        #serial_MDB.write('\x0C\xFF\xFF\xFF\xFF')	# Habilitar Monedero MDB
	#time.sleep(0.50)

	serial_MDB.close()
        serial_Display.close()

#main()
