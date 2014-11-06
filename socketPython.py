# -*- coding: utf-8 -*-
from libSocket import Socket, iniciarSocketC
import class_db
import InhibirMDB


__ACTIVO__ = '1'
__INACTIVO__ = '0'

if __name__ == "__main__":
	try:
		iniciarSocketC()
	except (KeyboardInterrupt, SystemExit):
		class_db.estadoSocketC(__INACTIVO__)
	try:
		Socket()
	except (KeyboardInterrupt, SystemExit):
		InhibirMDB.main()
		class_db.estadoSocketPython(__INACTIVO__)
