
import serial

INITIAL_MODBUS	= 0xFFFF
INITIAL_DF1		= 0x0000
BUFFER_SIZE		= 1024

# crc16_Init() - Initialize the CRC-16 table (crc16_Table[])
def init_table( ):
    # Initialize the CRC-16 table,
    #   build a 256-entry list, then convert to read-only tuple
    global table
    lst = []
    for i in range(256):
        data = i << 1
        crc = 0
        for j in range(8, 0, -1):
            data >>= 1
            if (data ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
        lst.append( crc)
    table = tuple( lst)
    return


def swap_bytes(word_val):
    """swap lsb and msb of a word"""
    msb = word_val >> 8
    lsb = word_val % 256
    return (lsb << 8) + msb


def calculate_crc(data):
    """Calculate the CRC16 of a datagram"""
    crc = 0xFFFF
    for i in data:
        crc = crc ^ ord(i)
        for j in xrange(8):
            tmp = crc & 1
            crc = crc >> 1
            if tmp:
                crc = crc ^ 0xA001
    return swap_bytes(crc)



def calc_chksum( st, crc):
	"""Calculate the CRC16 of a datagram"""
	for ch in st:
		crc = (crc >> 8) ^ table[(crc ^ ord(ch)) & 0xFF]
	return crc


def add_param( st, param ):
	rv = st +  "%c" %  chr( param )
	return rv


def add_chksum( st ):
	crc = calc_chksum ( st, INITIAL_MODBUS )
	rv = st + "%c%c" % ( ( crc & 0x00FF ), ( ( crc & 0xFF00 ) >> 8 ) )
	return rv


def convert_st( st , n):
	rv = ''
	if len(st) < n:
		for j in range(len(st) , n , 1):
			st += " ";
	if len(st) > 1:
		for j in range(0 , n , 2):
			rv += (st[j+1]) + (st[j])
	return rv


def to_int(st):
	rv = 0
	rv = ord(st[0])*0x0100 + ord(st[1])*0x0001
	return rv


def load_params (Params):
	
	Params.str_name		= 'MANUEL'		# Cliente - Nombre		- x0020 a x003F (32 a 63)
	Params.str_phone	= '464658459'	# Cliente - Telefono	- x0040 a x005F (64 a 95)
	Params.str_RFC		= '3243-445654-RET' # Cliente - RFC		- x0060 a x007F (96 a 127)
	Params.str_type		= 'Credito'		# Cliente - Tipo		- x0080 a x009F (128 a 159)
	Params.str_ID		= '1966'		# Vehiculo - ID			- x00A0 a x00BF (160 a 191)
	Params.str_model	= '1111'		# Vehiculo - Modelo		- x00C0 a x00DF (192 a 223)
	Params.str_credit	= '1000000.0'	# Vehiculo - Saldo		- x00E0 a x00FF (224 a 255)
	Params.str_plate	= 'P-45611111'	# Vehiculo - Placas		- x0100 a x011F (256 a 287)
	Params.str_econum	= '12345'		# Vehiculo - Num. Eco	- x0120 a x013F (288 a 319)
	Params.str_operator	= '1234-MANUEL'	# Vehiculo - Operador	- x0140 a x015F (320 a 351)
	Params.str_trademark= 'FORD'		# Vehiculo - Marca		- x0160 a x017F (352 a 383)
	Params.str_points	= '0'			# Vehiculo - Puntos		- x0180 a x019F (384 a 415)
	Params.str_operate_by = '7710 - PERISUR EXPRESS SA DE CV - ALSA 1' # x01A0 a x01DF (416 a 479)
	#Params.n_disp = 8

	Params.new_str_RFC1			= 'PEHJ'					# Cliente - RFC parte 1	- x0200 a x021F (512 a 543)	4
	Params.new_str_RFC2			= '620426'					# Cliente - RFC	parte 2	- x0220 a x023F (544 a 575)	6
	Params.new_str_RFC3			= 'D30'						# Cliente - RFC	parte 3	- x0240 a x025F (576 a 607)	4
	Params.new_str_name			= 'JUAN MANUEL PEREZ HERRERA'# Cliente - Nombre		- x0260 a x027F (608 a 639)	32
	Params.new_str_street		= 'GENERAL IGNACIO MARTINEZ'# Cliente - calle		- x0280 a x029F (640 a 671)	32
	Params.new_str_ext_number	= '1316'					# Cliente - Num. ext	- x02A0 a x02BF (672 a 703)	6
	Params.new_str_int_number	= ''						# Cliente - Num. int	- x02C0 a x02DF (704 a 735)	6
	Params.new_str_district		= 'TEQUISQUIAPAN'			# Cliente - Colonia		- x02E0 a x02FF (736 a 767)	30
	Params.new_str_county		= 'SAN LUIS POTOSI'			# Cliente - Municipio	- x0300 a x031F (768 a 799)	30
	Params.new_str_state		= 'S.L.P.'					# Vehiculo - estado		- x0320 a x033F (800 a 831)	20
	Params.new_str_zipcode		= '78230'					# Vehiculo - CP			- x0340 a x035F (832 a 863)	6
	Params.new_str_phone		= ''						# Vehiculo - telefono	- x0360 a x037F (864 a 895)	12
	Params.new_str_email1		= 'juanmaph@gmail.com'		# Vehiculo - Email 1	- x0380 a x039F (896 a 927)	20
	Params.new_str_email2		= ''						# Vehiculo - Email 2	- x03A0 a x03BF (928 a 959)	20

	return Params


def init_HMIPort (Device):
	return serial.Serial( Device.port,
								Device.baudrate,
								Device.bytesize,
								Device.parity,
								Device.stopbits,
								Device.timeout )

def	open_HMIPort( serial ):
	serial.open()


def	close_HMIPort( serial ):
	serial.close()


def poll (serial, Params):
		data = serial.readline()
		if ( data <> '' and len(data) > 1 ):
			#print 'Recibido ', repr(data[:])
			cmd	= data[1]
			options.get(cmd, unknown ) (serial, data, Params)


def read_coil(serial, data, Params):
	rv = 1
	if Params.n_disp > 16:
		Params.n_disp = 16
	for j in range(0 , Params.n_disp , 1):
		rv *= 2
	 #print "No. para dispensarios " , Params.n_disp,  rv-1
	SRT  = "\x01\x01\x02"


	SRT  +=  "%c%c" % ( (rv-1)%0x0100 , (rv-1)/0x0100 )


	SRT = add_chksum (SRT)
	#print rv, repr(SRT)
	serial.write(SRT)
	#return SRT

def read_discrete_input(serial):
	print "funcion \n"

def read_holding_register(serial, data, Params):

	device		= data[0]  # dispositivo
	start_reg	= to_int(data[2]+data[3])  # inicio de cadena
	num_reg		= (  ord(data[5]) )*2  # No. de registros en bytes
	#print num_reg
	
	if device == '\x01' and num_reg < 255 :	#Solicitud de datos por parte de pantalla HMI
		if   start_reg == 0x0000 :	STR  = Params.str_NAME + Params.str_VERSION
		elif start_reg == 0x0020 :	STR  = Params.str_name
		elif start_reg == 0x0040 :	STR  = Params.str_phone
		elif start_reg == 0x0060 :	STR  = Params.str_RFC
		elif start_reg == 0x0080 :	STR  = Params.str_type
		elif start_reg == 0x00A0 :	STR  = Params.str_ID
		elif start_reg == 0x00C0 :	STR  = Params.str_model
		elif start_reg == 0x00E0 :	STR  = Params.str_credit
		elif start_reg == 0x0100 :	STR  = Params.str_plate
		elif start_reg == 0x0120 :	STR  = Params.str_econum
		elif start_reg == 0x0140 :	STR  = Params.str_operator
		elif start_reg == 0x0160 :	STR  = Params.str_trademark
		elif start_reg == 0x0180 :	STR  = Params.str_points
		elif start_reg == 0x01A0 :	STR  = Params.str_operate_by

		elif start_reg == 0x0200 :	STR  = Params.new_str_RFC1
		elif start_reg == 0x0220 :	STR  = Params.new_str_RFC2
		elif start_reg == 0x0240 :	STR  = Params.new_str_RFC3
		elif start_reg == 0x0260 :	STR  = Params.new_str_name
		elif start_reg == 0x0280 :	STR  = Params.new_str_street
		elif start_reg == 0x02A0 :	STR  = Params.new_str_ext_number
		elif start_reg == 0x02C0 :	STR  = Params.new_str_int_number
		elif start_reg == 0x02E0 :	STR  = Params.new_str_district
		elif start_reg == 0x0300 :	STR  = Params.new_str_county
		elif start_reg == 0x0320 :	STR  = Params.new_str_state
		elif start_reg == 0x0340 :	STR  = Params.new_str_zipcode
		elif start_reg == 0x0360 :	STR  = Params.new_str_phone
		elif start_reg == 0x0380 :	STR  = Params.new_str_email1
		elif start_reg == 0x03A0 :	STR  = Params.new_str_email2
		else :						STR  = ""

		STR_cmp = '\x01\x03' + "%c%s"  %( num_reg , convert_st( STR, num_reg ) )
		STR_cmp = add_chksum (STR_cmp)
		serial.write(STR_cmp)


def read_input_register(serial):
	kbd = raw_input('Ingresar numero: ')
	print kbd
	SRT  = "\x01\x04\x02" + "%c%c" % (int(kbd)/256,int(kbd)%256 )
	SRT= add_chksum (SRT)
	serial.write(SRT)


def write_single_coil(serial, data, Params):
	start_reg = data[3]  #inicio de cadena
	if data[4] == '\xFF':
		value = 1
	else:
		value = 0
	if   start_reg == '\x00':
		Params.coil_001 = value
	elif start_reg == '\x01':
		Params.coil_002 = value
	elif start_reg == '\x02':
		Params.coil_003 = value
	elif start_reg == '\x03':
		Params.coil_004 = value
	print "Coils: %d  %d  %d  %d" % ( Params.coil_001, Params.coil_002, Params.coil_003, Params.coil_004 )
	SRT = "\x01\x05\x00%c%c\x00" % ( start_reg, data[4] )
	SRT = add_chksum (SRT)
	serial.write(SRT)


def write_single_register(serial):
	print "funcion \n"
def read_exception_status(serial):
	print "funcion \n"
def diagnostics(serial):
	print "funcion \n"
def write_multiple_coils(serial):
	print "funcion \n"
def write_multiple_registers(serial, data, Params):
	start_reg = data[3]  #inicio de cadena

	if   start_reg == '\x00' :	#	Pesos
		Params.in_00 =   (ord(data[7]) << 8) + ord(data[8])
		print 'Recibido: $  %d.%d ' % ( Params.in_00/100, Params.in_00%100), repr(data[:])
		Params.in_01 = ( Params.in_00*100 / Params.in_02*100 )/100	# Multiplica litros por precio
	elif   start_reg == '\x01' :	#	Litros
		Params.in_01 =   (ord(data[7]) << 8) + ord(data[8])
		print 'Recibido: %d.%d   Litro(s)' % ( Params.in_01/100, Params.in_01%100), repr(data[:])
		Params.in_00 = ( Params.in_01 * (Params.in_02) )/100	# Multiplica litros por precio
	elif   start_reg == '\x02' :	#	Magna
		Params.in_02 =   (ord(data[7]) << 8) + ord(data[8])
		Params.in_00 = ( Params.in_01 * (Params.in_02) )/100	# Multiplica litros por precio
		print 'Recibido: $%d.%02d  Magna' % ( Params.in_02/100, Params.in_02%100), repr(data[:])
	elif   start_reg == '\x03' :	#	Premium
		Params.in_03 =   (ord(data[7]) << 8) + ord(data[8])
		#Params.in_00 = ( Params.in_01 * (Params.in_02) )/1000	# Multiplica litros por precio
		print 'Recibido: $%d.%02d  Premium' % ( Params.in_03/100, Params.in_03%100), repr(data[:])
	elif   start_reg == '\x1d' :	#	cadena de datos (30 caracteres)
		Params.str_00 = convert_st(data[7:37])
		print 'Cadena 0:  ', Params.str_00 ,  repr(data[:])
	elif   start_reg == '\x3b' :	#	cadena de datos (30 caracteres)
		Params.str_01 = convert_st(data[7:37])
		print 'Cadena 1:  ', Params.str_01 ,  repr(data[:])
	else:
		print 'Recibido   ',  repr(data[:])
	SRT  = "\x01\x10\x00\x00\x00\x04"
	SRT= add_chksum (SRT)
	serial.write(SRT)


def read_file_record(serial):
	print "funcion \n"
def write_file_record(serial):
	print "funcion \n"
def rw_multiple_registers(serial):
	print "funcion \n"
def unknown(serial, data, Params):
	print "Comando Desconocido \n"

# Comandos de protocolo Modbus
options  ={	'\x01' : read_coil,
			'\x02' : read_discrete_input,
			'\x03' : read_holding_register,
			'\x04' : read_input_register,
			'\x05' : write_single_coil,
			'\x06' : write_single_register,
			'\x07' : read_exception_status,
			'\x08' : diagnostics,
			'\x0f' : write_multiple_coils,
			'\x10' : write_multiple_registers,
			'\x14' : read_file_record,
			'\x15' : write_file_record,
			'\x17' : rw_multiple_registers
}
