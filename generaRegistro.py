#-*- coding:utf-8 -*-
import datetime
import class_db
import time 


numSerie = "AC10TX1241213172"
shift = "1"
dateTime = "2014-11-04 10:48:30"
datetimesell = datetime.datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
ticket = 1
status = 0
rate = 3
multiplier = 1
cost = "3.00"
deposit = "3.00"
#denomDeposit = values_sell[10]   # Denominación del deposito
#cost_cal = float(rate) * float(multiplier)	
# archivo = open("/home/aramirez/Escritorio/registros.txt", "w")

fecha = "2014-11-04 "
hora = 10
minutos = 48
segundos = 30


for i in range(0,50000):
	datetimesell = str(fecha + str(hora) +':'+ str(minutos) +':'+ str(segundos))
	panelcat = "INSERT INTO panelcat(shiftno, serialnumber)"\
	            "VALUES('" + str(shift) + "', '" + str(numSerie) + "');"

	servicesdetail = "INSERT INTO servicesdetail(panelservicesid, rate, multiplier, cost) VALUES(" \
	"'" + str(ticket) + "', " \
	"'" + str(rate) + "', " \
	"'" + str(multiplier) + "'," \
	"'" + str(cost) + "');"

	panelservices = "INSERT INTO panelservices(cost, deposit, ticket, datetimesell, localshift, status) " \
	"VALUES('" + str(cost) + "'," \
	" '" + str(deposit) + "', " \
	"'" + str(ticket) + "', " \
	"'" + str(datetimesell) + "', " \
	"'" + str(shift) + "'," \
	"'" + str(status) +"');"

	config = "UPDATE config SET no_venta_act = '" + str(ticket) + "' WHERE no_serie_acceso = 1;"
	# archivo.write(panelcat)
	# archivo.write('\n')
	# archivo.write(panelservices)
	# archivo.write('\n')
	# archivo.write(servicesdetail)
	# archivo.write('\n')
	# archivo.write(config)
	# archivo.write('\n')
	
	class_db.insertar_venta(panelcat)
	class_db.insertar_venta(panelservices)
	class_db.insertar_venta(servicesdetail)
	class_db.insertar_venta(config)
	
	ticket += 1
	segundos += 1
	if segundos == 60:
		minutos += 1
		segundos = 0
	if minutos == 60:
		hora +=1
		minutos = 0

#archivo.close()
