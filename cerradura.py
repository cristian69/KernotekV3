import modbus
import serial
import time
import class_db
import logger

DEVICE = 0x01
COMMAND = 0x05
ADDR_HI = 0x00
ADDR_LO = 0x01
CMD_ON	= "\xFF\x00"
CMD_OFF	= "\x00\x00"


if __name__ == '__main__':
    try:    
	oneWire = serial.Serial('/dev/ttyUSBSMARTButton', 115200, timeout = 1)
	expander = serial.Serial('/dev/ttyUSBExpander', 9600  , timeout = 0.1)
	#oneWire.open ()
	#expander.open  ()
        class_db.estadoCerradura('1')
	modbus.init_table ()
	rv = ''
	rv = modbus.add_param (rv, DEVICE )
	rv = modbus.add_param (rv, COMMAND )
	rv = modbus.add_param (rv, ADDR_HI )
	rv = modbus.add_param (rv, ADDR_LO )
	while True:
		data = oneWire.readline()
		if ( data <> '' and len(data) > 8 and len(data) < 16  ):
			#print 'Recibido ', repr(data[:]) , (data [:-2])
                        data = data[:-2]
			estadoLlave = class_db.consultKey(data) 	
			if ( estadoLlave ):
				logger.cerradura("28| ABIERTO POR LLAVE " + str(data))
				#print 'Aprobado '			
				rv1 = rv + CMD_ON
				rv1 = modbus.add_chksum (rv1)
				expander.write(rv1)	#Encender bobina 1
				#print 'Enviando', repr(rv1)
				#expander.write("\x01\x05\x00\x00\xFF\x00\x8C\x3A")	#Encender bobina 1
				time.sleep(1)			
				rv2 = rv + CMD_OFF
				rv2 = modbus.add_chksum (rv2)
				expander.write(rv2)	#Encender bobina 1
				#print 'Enviando', repr(rv1)
				#expander.write("\x01\x05\x00\x00\x00\x00\xCD\xCA")	#Apagar bobina 1
			else:
				logger.cerradura("29| LLAVE NO ACEPTADA " + str(data))
				#print 'No Aprobado'
 		time.sleep(0.2)
    except(KeyboardInterrupt, SystemExit):
        class_db.estadoCerradura('0')
	oneWire.close()
	expander.close()
   


