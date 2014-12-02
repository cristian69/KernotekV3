function loadingPagina(parametro){
	if(parametro!=""){
		$("#paginaCargando").modal("show");
	}
}

function loading(){
	$("#paginaCargando").modal("show");
}



$(document).keypress(function(e) {
    if(e.which === 13) {
    	if($("#modalTarifa").hasClass("in")){
    		$(".btnAceptarCambioTarifa").click();
    		return false;
    	}
    	if($("#modalAcceso").hasClass("in")){
    		$("#aceptarCambioTarifa").click();
    		return false;
    	}
    }
});


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
		tarifaValida();
	}
}

function tarifaValida(){
	$("#tarifaIncorrecta").addClass("hidden");
	$("#tiempoIncorrecto").addClass("hidden");
	$("#aceptarCambioTarifa").click();
}






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
		accesoValido();
	}
}

function accesoValido(){
	$("#tarifaIncorrecta").addClass("hidden");
	$("#tiempoIncorrecto").addClass("hidden");
	$("#aceptarCambioTiempo").click();
}




function alertasiOcultar(parametro){
	$("#"+parametro).addClass("hidden");
}


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



function tablasReportes(parametro){

	if(parametro=="True"){
		$("#moduloFechas").addClass("hidden");
	}
	else{
		$("#moduloFechas").removeClass("hidden");
	}
}


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


$("#btnreporteFechas").click(function(){
	$(".fechasReporte").removeClass("hidden");
	$(".seleccionReporte").addClass("hidden");
	$("#inpTipoReporte").val("fechas");
	$(".footerModalReporte").removeClass("hidden");
});

$("#btnreporteTurno").click(function(){
	$(".fechasReporte").removeClass("hidden");
	$(".seleccionReporte").addClass("hidden");
	$("#inpTipoReporte").val("turno");
	$(".footerModalReporte").removeClass("hidden");
	$(".labelHoraInicio").addClass("hidden");
	$(".inputHoraInicio").addClass("hidden");
	$(".labelHoraFin").addClass("hidden");
	$(".inputHoraFin").addClass("hidden");
});

$("#regresarReporte").click(function(){
	$(".fechasReporte").addClass("hidden");
	$(".seleccionReporte").removeClass("hidden");
	$("#inpTipoReporte").val("");
	$(".footerModalReporte").addClass("hidden");
	$(".labelHoraInicio").removeClass("hidden");
	$(".inputHoraInicio").removeClass("hidden");
	$(".labelHoraFin").removeClass("hidden");
	$(".inputHoraFin").removeClass("hidden");
});

$("#aceptarReporte").click(function(){
	if($("#hora_inicio").val()=="" || $("#fecha_inicio").val()=="" || $("#hora_fin").val()=="" || $("#fecha_fin").val()==""){
		$("#errorFechas").removeClass("hidden");
		return false;
	}
});





$("#reporteTurnoSiguiente").click(function(){
	if($("#hora_inicio2").val()=="" || $("#fecha_inicio2").val()=="" || $("#hora_fin2").val()=="" || $("#fecha_fin2").val()==""){
		$("#errorFechas2").removeClass("hidden");
		return false;
	}
	else{
		$("#reporteTurno1").removeClass("active");
		$("#reportetabTurno1").removeClass("active");
		$("#reporteTurno2").addClass("active");
		$("#reportetabTurno2").addClass("active");
		$("#reporteTurnoAnterior").removeClass("hidden");
		$("#reporteTurnoSiguiente").addClass("hidden");
		$("#reporteTurnoAceptar").removeClass("hidden");		
	}
});

$("#reporteTurnoAnterior").click(function(){
	$("#reporteTurno1").addClass("active");
		$("#reportetabTurno1").addClass("active");
		$("#reporteTurno2").removeClass("active");
		$("#reportetabTurno2").removeClass("active");
		$("#reporteTurnoAnterior").addClass("hidden");
		$("#reporteTurnoSiguiente").removeClass("hidden");
		$("#reporteTurnoAceptar").addClass("hidden");
});




/*Acciones que se realiara si se selecciona la opcion de corte,
configureacion o cambiar tipo de corte de turno*/
$("#btnCorte").click(function(){
	$("#Turno1").removeClass("active")
	$("#Turno2b").addClass("active")
	$(".footerCorteTurno").removeClass("hidden");
	$("#AceptarCorte").removeClass("hidden");
	$("#CancelarCorte").removeClass("hidden");
	$("#valorPestaña").val("4");
});

$("#CancelarCorte").click(function(){
	if($("#valorPestaña").val()=="1" || $("#valorPestaña").val()=="4"){
		$("#Turno2b").removeClass("active");
		$("#Turno1").addClass("active");
		$(".footerCorteTurno").addClass("hidden");
		$("#CancelarCorte").addClass("hidden");
		$("#ConfirmarAccionT").addClass("hidden");
		$("#turno2").removeClass("active");
		$("#AceptarCorte").addClass("hidden");
		$("#valorPestaña").val("1");
		$("#accion").val("");
	}
});


$("#btnConfigurar").click(function(){
	$("#turno2").addClass("active");
	$("#Turno1").removeClass("active");
	$(".footerCorteTurno").removeClass("hidden");
	$("#AceptarCorte").removeClass("hidden");
	$("#CancelarCorte").removeClass("hidden");
	$("#accion").val("configurar");
});


$("#btnCambiarCorte").click(function(){
	if($("#valorPestaña").val()=="1"){
		$("#pasoTurno2a").addClass("active");
		$("#pasoTurno2a").removeClass("hidden");
		$("#Turno2a").addClass("active");
		$("#pasoTurno1").removeClass("active");
		$("#Turno1").removeClass("active");	
		$("#anteriorCorte").removeClass("hidden");
		$(".footerCorteTurno").removeClass("hidden");
		$("#valorPestaña").val("2");
		$("#accion").val("manual");	
	}
});



$("#btnAutomaticoCorte").click(function(){
	$("#pasoTurno2a").removeClass("active");
	$("#Turno2a").removeClass("active");		
	$("#pasoTurno3a").addClass("active");
	$("#pasoTurno3a").removeClass("hidden");
	$("#turno2").addClass("active");
	$("#siguienteCorte").addClass("hidden");
	$("#ConfirmarAccionT").removeClass("hidden");
	$("#valorPestaña").val("3");
	$("#accion").val("automatico");
});

$("#anteriorCorte").click(function(){
	if($("#valorPestaña").val()=="2"){
		$("#pasoTurno2a").removeClass("active");
		$("#pasoTurno2a").addClass("hidden");
		$("#Turno2a").removeClass("active");
		$("#pasoTurno1").addClass("active");
		$("#Turno1").addClass("active");	
		$("#anteriorCorte").addClass("hidden");
		$(".footerCorteTurno").addClass("hidden");
		$("#valorPestaña").val("1");
		$("#accion").val("");
	}


$("#anteriorCorte").click(function(){
	if($("#valorPestaña").val()!="1" && $("#valorPestaña").val()!="2"){
		$("#pasoTurno2a").addClass("active");
		$("#pasoTurno2a").removeClass("hidden");
		$("#Turno2a").addClass("active");
		$("#pasoTurno1").removeClass("active");
		$("#Turno1").removeClass("active");	
		$("#anteriorCorte").removeClass("hidden");
		$(".footerCorteTurno").removeClass("hidden");
		$("#valorPestaña").val("2");


		$("#pasoTurno2a").addClass("active");
	$("#Turno2a").addClass("active");		
	$("#pasoTurno3a").removeClass("active");
	$("#pasoTurno3a").addClass("hidden");
	$("#turno2").removeClass("active");
	$("#siguienteCorte").removeClass("hidden");
	$("#ConfirmarAccionT").addClass("hidden");
	$("#accion").val("manual");
	}
});



});






$("#modalTurno").mouseover(function(){
	if($("#Lapso").val()!="cadaSemana" && $("#Lapso").val()!="cadaMes"){
		document.getElementById("labelTipoCorte").innerHTML = "Hora del día para la realización del corte de turno";
		$("#semana").addClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").removeClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaSemana"){
		document.getElementById("labelTipoCorte").innerHTML = "Día de la semana y hora para la realización del corte de turno";
		$("#semana").removeClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaMes"){
		document.getElementById("labelTipoCorte").innerHTML = "Día del mes y hora para la realización del corte de turno";
		$("#semana").addClass("hidden");
		$("#mes").removeClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
});

$(".configuracionCortes").mouseover(function(){
	if($("#Lapso").val()!="cadaSemana" && $("#Lapso").val()!="cadaMes"){
		document.getElementById("labelTipoCorte").innerHTML = "Hora del día para la realización del corte de turno";
		$("#semana").addClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").addClass("hidden");
		$(".contenedorFecha").removeClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaSemana"){
		document.getElementById("labelTipoCorte").innerHTML = "Día de la semana y hora para la realización del corte de turno";
		$("#semana").removeClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").removeClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaMes"){
		document.getElementById("labelTipoCorte").innerHTML = "Día del mes y hora para la realización del corte de turno";
		$("#semana").addClass("hidden");
		$("#mes").removeClass("hidden");
		$(".contenedorFecha").removeClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
});

$(".configuracionCortes").mouseover(function(){
	if($("#seleccionarAccion").val()=="cambiar" && $("#tiposCortes").val()=="manual" && $("#banderaPosicion").val()=="2"){
		$("#cancelarAccion").removeClass("hidden");
		$("#aceptarAccion").removeClass("hidden");
		$("#nextTurno").addClass("hidden");
		$("#backTurno").addClass("hidden");
	}
	if($("#seleccionarAccion").val()=="cambiar" && $("#tiposCortes").val()=="automatico"){
		$("#cancelarAccion").addClass("hidden");
		$("#aceptarAccion").addClass("hidden");
		$("#nextTurno").removeClass("hidden");	
		$("#backTurno").removeClass("hidden");
	}
});


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






	$("#nextTurno").click(function(){
		if($("#seleccionarAccion2").val()=="corte" && $("#configurraCorte").hasClass("hidden")){
			$("#aAccion").removeClass("hidden");
			$("#cAccion").removeClass("hidden");
			$("#nextTurno").addClass("hidden");
			$("#mturno2").addClass("active");
			$("#paso2").addClass("active");
			$("#mturno1").removeClass("active");
			$("#paso1").removeClass("active");
			$("#paso2").removeClass("hidden");
		}

		if($("#seleccionarAccion2").val()=="configurar" && $("#hacerCorte").hasClass("hidden")){
			$("#paso4").removeClass("hidden");
			$("#paso4").addClass("active");
			$("#mturno4").addClass("active");
			$("#mturno1").removeClass("active");
			$("#paso1").removeClass("active");
			$("#aAccion").removeClass("hidden");
			$("#cAccion").removeClass("hidden");
			$("#nextTurno").addClass("hidden");
		}
		if($("#seleccionarAccion2").val()=="cambiar"){
			$("#paso3").addClass("active");
			$("#paso3").removeClass("hidden");
			$("#mturno3").addClass("active");
			$("#paso1").removeClass("active");
			$("#mturno1").removeClass("active");
			$("#backTurno").removeClass("hidden");
			$("#banderaPosicion").val("2");
		}
		if($("#seleccionarAccion2").val()=="cambiar" && $("#tiposCortes2").val()=="automatico"){
			$("#paso3").removeClass("active");
			$("#mturno3").removeClass("active");
			$("#paso4").addClass("active");
			$("#paso4").removeClass("hidden");
			$("#mturno4").addClass("active");
			$("#nextTurno").addClass("hidden");
			$("#aAccion").removeClass("hidden");
			$("#banderaPosicion").val("3");
		}
	});






	/*Cancelar el corte manual*/
	$("#cAccion").click(function(){
		if($("#seleccionarAccion2").val()=="corte"){
			$("#aAccion").addClass("hidden");
			$("#cAccion").addClass("hidden");
			$("#nextTurno").removeClass("hidden");
			$("#mturno2").removeClass("active");
			$("#paso2").removeClass("active");
			$("#mturno1").addClass("active");
			$("#paso1").addClass("active");
			$("#paso2").addClass("hidden");
		}
		if($("#seleccionarAccion2").val()=="configurar"){
			$("#paso4").addClass("hidden");
			$("#paso4").removeClass("active");
			$("#mturno4").removeClass("active");
			$("#mturno1").addClass("active");
			$("#paso1").addClass("active");
			$("#aAccion").addClass("hidden");
			$("#cAccion").addClass("hidden");
			$("#nextTurno").removeClass("hidden");	
		}
	});


	$("#backTurno").click(function(){
		if($("#seleccionarAccion2").val()=="cambiar" && $("#banderaPosicion").val()=="2"){
			$("#paso3").removeClass("active");
			$("#paso3").addClass("hidden");
			$("#mturno3").removeClass("active");
			$("#mturno3").removeClass("active");
			$("#paso1").addClass("active");
			$("#mturno1").addClass("active");
			$("#backTurno").addClass("hidden");
			$("#aCorte").addClass("hidden");
			$('#tiposCortes2 > option[value=""]').attr('selected', 'selected');
			$("#tiposCortes2").select2({
				placeholder: "Selecciona el tipo de corte de turno"
			});
			$("#nextTurno").removeClass("hidden");


			$("#banderaPosicion").val("1")
		}
		if($("#seleccionarAccion2").val()=="cambiar" && $("#tiposCortes2").val()=="automatico" && $("#banderaPosicion").val()!="1"){
			$("#paso3").addClass("active");
			$("#mturno3").addClass("active");
			$("#paso4").removeClass("active");
			$("#paso4").addClass("hidden");
			$("#mturno4").removeClass("active");
			$("#nextTurno").removeClass("hidden");
			$("#aAccion").addClass("hidden");
			$('#tiposCortes2 > option[value=""]').attr('selected', 'selected');
			$("#tiposCortes2").select2({
				placeholder: "Selecciona el tipo de corte de turno"
			});
			$("#banderaPosicion").val("2");
		}

		
	});

$(".configuracionCortes").mouseover(function(){
	if($("#seleccionarAccion2").val()=="cambiar" && $("#banderaPosicion").val()=="2" && $("#tiposCortes2").val()=="manual"){
		$("#aCorte").removeClass("hidden");
		$("#nextTurno").addClass("hidden");
	}
	if($("#seleccionarAccion2").val()=="cambiar" && $("#banderaPosicion").val()=="2" && $("#tiposCortes2").val()!="manual"){
		$("#aCorte").addClass("hidden");
		$("#nextTurno").removeClass("hidden");
	}

});