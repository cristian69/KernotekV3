
import serial
import time


def main():
        serial_MDB = serial.Serial('/dev/ttyUSBMDB', 9600, timeout = 0.1)

        serial_MDB.write('\x08')        #Resetear Monedero MDB
        #serial_MDB.write('\x0C\xFF\xFF\xFF\xFF')       # Habilitar Monedero MDB

        serial_MDB.close()
#main()

