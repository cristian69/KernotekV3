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
 * @method mostrarVentanas
 * @param {String} idventana
 * @return 
 */
function mostrarVentanas(idventana){
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
 * @method graficasHome
 * @param {String} grafica
 * @param {array} labels
 * @param {array} datos
 * @return 
 */
function graficasHome(grafica, labels, datos){
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
 * @method validarNumeros
 * @return false
 */
function validarNumeros(){
	numeroValidar=$("#nuevaTarifa").val();
	var patron1=/\s/;
	var patron2=/^[0-9]+(\.[0,5]{0,1})?$/;
	if(!patron2.test(numeroValidar) || $("#nuevaTarifa").val()=="" || patron1.test(numeroValidar)){
		$("#tarifaIncorrecta").removeClass("hidden");
		$("#nuevaTarifa").val("");
		$('#nuevaTarifa').focus();
		return false;
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
 * @method validarApertura
 * @return 
 */
function validarApertura(){
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
 * @method alertasiOcultar
 * @param {String} idAlerta
 * @return 
 */
function alertasiOcultar(idAlerta){
	$("#"+idAlerta).addClass("hidden");
}



/**
 * Muestra el botón de apagar o encender sistema de acuerdo al
 * parámetro introducido en la función, recibe un parámetro booleano,
 * si es TRUE es que el sistema está encendido y se mostrará el
 * botón de apagar, de lo contrario se mostrará el botón de  encender.
 * @method apagadoSistema
 * @param {} parametro
 * @return 
 */
function apagadoSistema(parametro){
	if(parametro=="True"){
		$("#btnApagar").removeClass("hidden");
		$("#btnEncender").addClass("hidden");
	}
	else{
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
 * @method reporteTurnos
 * @param {boolean} parametro1
 * @param {boolean} parametro2
 * @return 
 */
function reporteTurnos(parametro1, parametro2){
	if(parametro1=="True"){
		$("#descargarTurnoExcel").removeClass("hidden");
		$("#generarTurnoExcel").addClass("hidden");
	}
	if(parametro2=="True"){
		$("#descargarTurnoPdf").removeClass("hidden");
		$("#generarTurnoPdf").addClass("hidden");
	}
	if(parametro1=="False"){
		$("#descargarTurnoExcel").addClass("hidden");
		$("#generarTurnoExcel").removeClass("hidden");
	}
	if(parametro2=="False"){
		$("#descargarTurnoPdf").addClass("hidden");
		$("#generarTurnoPdf").removeClass("hidden");
	}

}


/**
 * Description
 * @method generarExcel
 * @param {} excelGeneral
 * @param {} excelEspecifico
 * @param {} excelDetallado
 * @param {} ventana
 * @return 
 */
function generarExcel(excelGeneral, excelEspecifico, excelDetallado, ventana){
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
 * Description
 * @method tablasReportes
 * @param {} parametro
 * @return 
 */
function tablasReportes(parametro){
	if(parametro=="True"){
		$("#moduloFechas").addClass("hidden");
		$(".nuevoReporte").removeClass("hidden");
	}
	else{
		$("#moduloFechas").removeClass("hidden");
	}
}


/**
 * Description
 * @method corteValores
 * @param {} parametro
 * @return 
 */
function corteValores(parametro){
	if(parametro=='Manual'){
		$('#btnConfigurar').addClass("hidden");
		$("#btnCorte").removeClass("hidden");
	}
	if(parametro=="Automático"){
		$('#btnConfigurar').removeClass("hidden");
		$("#btnCorte").addClass("hidden");
	}
}


/**
 * Description
 * @method valoresTurnoh
 * @return 
 */
var valoresTurnoh=function(){
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