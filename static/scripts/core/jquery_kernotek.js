/**
 * Muestra las modales de cambio de tarifa y cambio de 
 * iempo en el acceso, y posiciona el cursor en el INPUT
 * correspondiente a la modal que está visible.
 * @method viewModals
 * @return 
 */
function viewModals(){
	$('#modalTarifa').on('shown.bs.modal', function () {
		$('#nuevaTarifa').val("");
    	$('#nuevaTarifa').focus()
	})
	$('#modalAcceso').on('shown.bs.modal', function () {
		$('#nuevoTiempo').val("");
    	$('#nuevoTiempo').focus();
	})
}


/**
 * Muestra las alertas cuyo ID sea idéntico al valor del
 * parámetro dado a la funcion.
 * @method showWindow
 * @param {String} idventana
 * @return 
 */
function showWindow(idventana){
	this.nombreVentana=idventana;
	$("#"+nombreVentana).removeClass("hidden");
	if(nombreVentana!=""){
		$(".contentAlerttas").removeClass("hidden");
	}
	if(nombreVentana=="UsuarioInvalido"){
		$("#contenidoLogin").addClass("errorLogin");
	}
}


/**
 * Esta función se encuentra vinculada al plugin chart.js,
 * recibe tres parámetros, uno es el nombre de la gráfica
 * a generar, y dos parámetros tipo arreglo, uno que contiene
 * las cantidades a graficar y otro que contiene las etiquetas
 * de la gráfica.
 * @method startGraphics
 * @param {String} grafica
 * @param {array} labels
 * @param {array} datos
 * @return 
 */
function startGraphics(grafica, labels, datos){
	if(grafica=="graficaDia"){
		$("#diaria").addClass("active");
		$("#graficaenDias").addClass("active");
		$("#semanal").removeClass("active");
		$("#graficaenSemanas").removeClass("active");
		$("#mensual").removeClass("active");
		$("#graficaenMeses").removeClass("active");
		var data1 = {
			labels : [labels[0],labels[1],labels[2],labels[3],labels[4],labels[5],labels[6]],
			datasets : [
			{
				label: "Ganancias en pesos",
				fillColor : "rgba(220,220,220,0.2)",
				strokeColor : "#009DE0",
				pointColor : "rgba(151,187,205,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(0,247,247,1)",
				data : [datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6]]
			}
			]
		}
		var lineChartData1 = new Chart(document.getElementById("graficaDia").getContext("2d")).Line(data1,{responsive:true});
		document.getElementById("labelDias").innerHTML = lineChartData1.generateLegend();
	}
	if(grafica=="graficaSemana"){
		$("#diaria").removeClass("active");
		$("#graficaenDias").removeClass("active");
		$("#semanal").addClass("active");
		$("#graficaenSemanas").addClass("active");
		$("#mensual").removeClass("active");
		$("#graficaenMeses").removeClass("active");
		var data2 = {
			labels : [labels[0],labels[1],labels[2],labels[3],labels[4],labels[5],labels[6]],
			datasets : [
			{
				label: "Ganancias en pesos",
				fillColor : "rgba(220,220,220,0.2)",
				strokeColor : "#009DE0",
				pointColor : "rgba(151,187,205,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(0,247,247,1)",
				data : [datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6]]
			}
			]
		}
		var lineChartData2 = new Chart(document.getElementById("graficaSemana").getContext("2d")).Line(data2,{responsive:true});
		document.getElementById("labelSemana").innerHTML = lineChartData2.generateLegend();
	}
	if(grafica=="graficaMes"){
		$("#diaria").removeClass("active");
		$("#graficaenDias").removeClass("active");
		$("#semanal").removeClass("active");
		$("#graficaenSemanas").removeClass("active");
		$("#mensual").addClass("active");
		$("#graficaenMeses").addClass("active");
		var data3 = {
			labels : [labels[0],labels[1],labels[2],labels[3],labels[4],labels[5],labels[6]],
			datasets : [
			{
				label: "Ganancias en pesos",
				fillColor : "rgba(220,220,220,0.2)",
				strokeColor : "#009DE0",
				pointColor : "rgba(151,187,205,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(0,247,247,1)",
				data : [datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6]]
			}
			]
		}
		var lineChartData1 = new Chart(document.getElementById("graficaMes").getContext("2d")).Line(data3,{responsive:true});
		document.getElementById("labelMes").innerHTML = lineChartData1.generateLegend();
	}
}


/**
 * Muestra la modal  “loading” para que el usuario
 * identifique que se esta procesando una petición en el
 * servidor.
 * @method loading
 * @return 
 */
function loading(){
	$("#paginaCargando").modal("show");
}


/**
 * Detecta si el ENTER ha sido presionado, dependiendo si
 * la modal de “Cambio de tarifa o cambio en el tiempo de
 * acceso”, evitará que se realice el submit y se presionara
 * automaticamente la funcion para validar dichos valores
 * servidor.
 * @method 
 * @return false
 */
$(document).keypress(function(e) {
    if(e.which === 13) {
    	if($("#modalTarifa").hasClass("in")){
    		$(".btnAceptarCambioTarifa").click();
    		return false;
    	}
    	if($("#modalAcceso").hasClass("in")){
    		$(".btnAceptarCambioTiempo").click();
    		return false;
    	}
    }
});


/**
 * Valida el número de la modal de cambio de tarifa antes de
 * mandarlo al servidor, identifica que sea número, que no tenga
 * espacios en blanco y que el formato sea correcto, si es
 * incorrecto detendrá el SUBMIT y mandara manda una alerta.
 * @method validateRate
 * @return false
 */
function validateRate(){
	numeroValidar=$("#nuevaTarifa").val();
	var patron1=/\s/;
	var patron2=/^[0-9]+(\.[0,5]{0,1})?$/;
	validacion=parseFloat(".5");
	if(!patron2.test(numeroValidar) || $("#nuevaTarifa").val()=="" || patron1.test(numeroValidar)){
		$("#tarifaIncorrecta").removeClass("hidden");
		$("#nuevaTarifa").val("");
		$('#nuevaTarifa').focus();
		return false;
	}
	if(numeroValidar<=validacion){
		$("#tarifaIncorrecta").removeClass("hidden");
		$("#nuevaTarifa").val("");
		$('#nuevaTarifa').focus();
		return false;
	}
	if(numeroValidar==".5"){
		$("#tarifaIncorrecta").addClass("hidden");
		$("#tiempoIncorrecto").addClass("hidden");
		$("#aceptarCambioTarifa").click();
	}
	else{
		$("#tarifaIncorrecta").addClass("hidden");
		$("#tiempoIncorrecto").addClass("hidden");
		$("#aceptarCambioTarifa").click();
	}
}


/**
 * Valida el número de la modal de cambio de tiempo en el acceso
 * antes de mandarlo al servidor, identifica que sea número, que no
 * tenga espacios en blanco y que el formato sea correcto, si es
 * incorrecto detendrá el SUBMIT y mandara manda una alerta.
 * @method validateTime
 * @return false
 */
function validateTime(){
	aperturaValidar=$("#nuevoTiempo").val();
	var patron1=/\s/;
	var patron2=/^[0-9]+$/;
	if(!patron2.test(aperturaValidar) || $("#nuevoTiempo").val()=="" || patron1.test(aperturaValidar)){
		$("#tiempoIncorrecto").removeClass("hidden");
		$("#nuevoTiempo").val("");
		$('#nuevoTiempo').focus();
		return false;
	}
	else{
		$("#tarifaIncorrecta").addClass("hidden");
		$("#tiempoIncorrecto").addClass("hidden");
		$("#aceptarCambioTiempo").click();
	}
}


/**
 * Oculta las alertas cuyo ID sea idéntico al parámetro dado en
 * la función.
 * @method hideAlerts
 * @param {String} idAlerta
 * @return 
 */
function hideAlerts(idAlerta){
	$("#"+idAlerta).addClass("hidden");
}



/**
 * Muestra el botón de apagar o encender sistema de acuerdo al
 * parámetro introducido en la función, recibe un parámetro booleano,
 * si es TRUE es que el sistema está encendido y se mostrará el
 * botón de apagar, de lo contrario se mostrará el botón de  encender.
 * @method stateSystem
 * @param {} estado
 * @return 
 */
function stateSystem(estado){
	if(estado=="True"){
		document.getElementById("pestadoSistema").innerHTML="Estado actual del sistema: Encendido";
		$("#btnApagar").removeClass("hidden");
		$("#btnEncender").addClass("hidden");
	}
	else{
		document.getElementById("pestadoSistema").innerHTML="Estado actual del sistema: Apagado";
		$("#btnApagar").addClass("hidden");
		$("#btnEncender").removeClass("hidden");
	}
}


/**
 * Inicializa las campos selects con el estilo del plugin “SELECT”.
 * @method home
 * @return 
 */
function home(){
	$("#accionRealizar").select2({
		placeholder:"Tipo de reporte"
	});
	$("#Lapso").select2();
	$("#semana").select2();
	$("#mes").select2();
	$("#tiposCortes").select2({
		placeholder: "Selecciona el tipo de corte de turno"
	});
	$("#tiposCortes2").select2({
		placeholder: "Selecciona el tipo de corte de turno"
	});
	$("#seleccionarAccion").select2({
		placeholder:"seleccionar acción"
	});
	$("#seleccionarAccion2").select2({
		placeholder:"seleccionar acción"
	});
}


/**
 * Recibe dos parámetros, dependiendo de ellos se mostrará
 * la opción de descargar el reporte, de lo contrario se
 * visualiza la opción para generarlo.
 * @method turnsReport
 * @param {} reporteExcel
 * @param {} reportePDF
 * @return 
 */
function turnsReport(reporteExcel, reportePDF){
	if(reporteExcel=="True"){
		$("#descargarTurnoExcel").removeClass("hidden");
		$("#generarTurnoExcel").addClass("hidden");
	}
	if(reportePDF=="True"){
		$("#descargarTurnoPdf").removeClass("hidden");
		$("#generarTurnoPdf").addClass("hidden");
	}
	if(reporteExcel=="False"){
		$("#descargarTurnoExcel").addClass("hidden");
		$("#generarTurnoExcel").removeClass("hidden");
	}
	if(reportePDF=="False"){
		$("#descargarTurnoPdf").addClass("hidden");
		$("#generarTurnoPdf").removeClass("hidden");
	}

}


/**
 * Dependiendo del valor de los parámetros, depende si se mostrara
 * la opcion para descargar el reporte o generar el reporte. Ademas
 * el parámetro ventana no indica el reporte que estará visible. 
 * @method generateExcel
 * @param {} excelGeneral
 * @param {} excelEspecifico
 * @param {} excelDetallado
 * @param {} ventana
 * @return 
 */
function generateExcel(excelGeneral, excelEspecifico, excelDetallado, ventana){
	if(excelGeneral=="True"){
		$("#linkgeneral").addClass("hidden");
		$("#descargargeneral").removeClass("hidden")
	}
	if(excelGeneral=="False"){
		$("#linkgeneral").removeClass("hidden");
		$("#descargargeneral").addClass("hidden")
	}
	if(excelEspecifico=="True"){
		$("#linkespecifico").addClass("hidden");
		$("#descargarespecifico").removeClass("hidden")
	}
	if(excelEspecifico=="False"){
		$("#linkespecifico").removeClass("hidden");
		$("#descargarespecifico").addClass("hidden")
	}
	if(excelDetallado=="True"){
		$("#linkdetallado").addClass("hidden");
		$("#descargardetallado").removeClass("hidden")
	}
	if(excelDetallado=="False"){
		$("#linkdetallado").removeClass("hidden");
		$("#descargardetallado").addClass("hidden")
	}
	if(ventana=="General"){
		$("#linkespecifico").removeClass("hidden");
	}
	if(ventana=="Específico"){
		$("#linkgeneral").removeClass("hidden");
	}
}


/**
 * Nos ayuda a identificar si en el módulo de reportes
 * se estará visualizando el reporte o el módulo de
 * fechas para generarlo, dependiendo de ello se visualiza
 * u oculta el módulo de las fechas.
 * @method chartReports
 * @param {} ventanaFechas
 * @return 
 */
function chartReports(ventanaFechas){
	if(ventanaFechas=="True"){
		$("#moduloFechas").addClass("hidden");
		$(".nuevoReporte").removeClass("hidden");
	}
	else{
		$("#moduloFechas").removeClass("hidden");
	}
}


/**
 * Identifica que tipo de corte de turno es el actual dependiendo
 * del parámetro dado, dependiendo del tipo de corte se visualizarán
 * las opciones de corte de turno (cuando es manual) o configurar
 * (cuando es automático).
 * @method cuttingType
 * @param {} tipoCorte
 * @return 
 */
function cuttingType(tipoCorte){
	if(tipoCorte=='Manual'){
		$('#btnConfigurar').addClass("hidden");
		$("#btnCorte").removeClass("hidden");
	}
	if(tipoCorte=="Automático"){
		$('#btnConfigurar').removeClass("hidden");
		$("#btnCorte").addClass("hidden");
	}
}


/**
 * Se asignan los valores actual del corte de turno
 * automático a los campo de los modulos.
 * @method configAutomatic
 * @return 
 */
var configAutomatic=function(){
		valorLapso=$(".tipoLapsoh").val();
    	valorSemana=$(".diaCorteh").val();
    	valorHora=$(".horaCorteh").val();
    	if(valorLapso=='Mensual'){
    		document.getElementById("labelTipoCorte").innerHTML = "Día del mes y hora para la realización del corte de turno";
        	$('#Lapso > option[value="cadaMes"]').attr('selected', 'selected');
	        $('#mes > option[value="'+valorSemana+'"]').attr('selected','selected');
	        $('#horaC').val(valorHora);
	        $('.contenedorFecha').addClass('col-md-6');
	        $('#mes').removeClass('hidden');
	        $('#semana').addClass('hidden');
	        $("#Lapso").select2();
			$("#semana").select2();
			$("#mes").select2();
	    }
	    if(valorLapso=='Semanal'){
	    	document.getElementById("labelTipoCorte").innerHTML = "Día de la semana y hora para la realización del corte de turno";
	        $('#Lapso > option[value="cadaSemana"]').attr('selected', 'selected');
	        $('#semana > option[value="'+valorSemana+'"]').attr('selected', 'selected');
	        $('#horaC').val(valorHora);
	        $('.contenedorFecha').addClass('col-md-6');
	        $('#semana').removeClass('hidden');
	        $('#mes').addClass('hidden');
	        $("#Lapso").select2();
			$("#semana").select2();
			$("#mes").select2();
	    }
	    if(valorLapso=='Diario'){
	    	document.getElementById("labelTipoCorte").innerHTML = "Hora del día para la realización del corte de turno";
	        $('#Lapso > option[value="cadaDia"]').attr('selected', 'selected');
	        $('#horaC').val(valorHora);
	        $('.contenedorFecha').removeClass('col-md-6');
	        $("#Lapso").select2();
			$("#semana").select2();
			$("#mes").select2();        
	    }
	    if(valorLapso=='cadaDetHora'){
	    	document.getElementById("labelTipoCorte").innerHTML = "Seleccionar cada cuantas horas se realizará el corte de turno";
	        $('#Lapso > option[value="cadaDetHora"]').attr('selected', 'selected');
	        $('#horaC').val(valorHora);
	        $('.contenedorFecha').removeClass('col-md-6');  
	        $("#Lapso").select2();
			$("#semana").select2();
			$("#mes").select2();          
	    }
	}