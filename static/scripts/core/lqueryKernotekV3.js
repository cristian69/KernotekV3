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
	$('input').iCheck({
    checkboxClass: 'icheckbox_square-blue',
    radioClass: 'iradio_square-blue',
    increaseArea: '80%'
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

function generarExcel(parametroExcel, parametroDetallado){
	if(parametroExcel=="True"){
		$("#excelDescargar").removeClass("hidden");
		$("#generarExcel").addClass("hidden");
	}
	if(parametroExcel=="False"){
		$("#excelDescargar").addClass("hidden");
		$("#generarExcel").removeClass("hidden");
	}
	if(parametroDetallado=="True"){
		$("#descargarDetallado").removeClass("hidden");
		$("#detallado").addClass("hidden");
	}
	if(parametroDetallado=="False"){
		$("#descargarDetallado").addClass("hidden");
		$("#detallado").removeClass("hidden");
	}
	if(parametroExcel!="True"){
		$("#excelDescargar").addClass("hidden");
		$("#generarExcel").removeClass("hidden");
	}
	if(parametroDetallado!="True"){
		$("#descargarDetallado").addClass("hidden");
		$("#detallado").removeClass("hidden");
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
	if(parametro=='aanual'){
		$('#btnConfigurar').addClass("hidden");
	}
	if(parametro=="automático"){
		$("#btnCorte").addClass("hidden")
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
});

$("#regresarReporte").click(function(){
	$(".fechasReporte").addClass("hidden");
	$(".seleccionReporte").removeClass("hidden");
	$("#inpTipoReporte").val("");
	$(".footerModalReporte").addClass("hidden");
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
	$("#Turno2b").addClass("active");
	$("#Turno1").removeClass("active");
	$(".footerCorteTurno").removeClass("hidden");
	$("#CancelarCorte").removeClass("hidden");
	$("#ConfirmarAccionT").removeClass("hidden");
});

$("#CancelarCorte").click(function(){
	if($("#valorPestaña").val()=="1"){
		$("#Turno2b").removeClass("active");
		$("#Turno1").addClass("active");
		$(".footerCorteTurno").addClass("hidden");
		$("#CancelarCorte").addClass("hidden");
		$("#ConfirmarAccionT").addClass("hidden");
		$("#turno2").removeClass("active");
		$("#AceptarCorte").addClass("hidden");
	}
});


$("#btnConfigurar").click(function(){
	$("#turno2").addClass("active");
	$("#Turno1").removeClass("active");
	$(".footerCorteTurno").removeClass("hidden");
	$("#AceptarCorte").removeClass("hidden");
	$("#CancelarCorte").removeClass("hidden");
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
	}
});



});


function validarNumeros(){
	numeroValidar=$("#nuevaTarifa").val();
	var patron1=/\s/;
	var patron2=/^[0-9]+(\.[0,5]{0,1})?$/;
	if(!patron2.test(numeroValidar) || $("#nuevaTarifa").val()=="" || patron1.test(numeroValidar)){
		$("#tarifaIncorrecta").removeClass("hidden");
		$("#nuevaTarifa").val("");
		return false;
	}
}

function validarApertura(){
	aperturaValidar=$("#nuevoTiempo").val();
	var patron1=/\s/;
	var patron2=/^[0-9]+$/;
	if(!patron2.test(aperturaValidar) || $("#nuevoTiempo").val()=="" || patron1.test(aperturaValidar)){
		$("#tiempoIncorrecto").removeClass("hidden");
		$("#nuevoTiempo").val("");
		return false;
	}
}


$("#modalTurno").mouseover(function(){
	if($("#Lapso").val()!="cadaSemana" && $("#Lapso").val()!="cadaMes"){
		document.getElementById("labelTipoCorte").innerHTML = "Hora del dia para la realización del corte de turno";
		$("#semana").addClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").removeClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaSemana"){
		document.getElementById("labelTipoCorte").innerHTML = "Dia de la semana y hora para la realizacion del corte de turno.";
		$("#semana").removeClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaMes"){
		document.getElementById("labelTipoCorte").innerHTML = "Dia del mes y hora para la realizacion del corte de turno.";
		$("#semana").addClass("hidden");
		$("#mes").removeClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
});

$(".configuracionCortes").mouseover(function(){
	if($("#Lapso").val()!="cadaSemana" && $("#Lapso").val()!="cadaMes"){
		document.getElementById("labelTipoCorte").innerHTML = "Hora del dia para la realización del corte de turno";
		$("#semana").addClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").removeClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaSemana"){
		document.getElementById("labelTipoCorte").innerHTML = "Dia de la semana y hora para la realizacion del corte de turno.";
		$("#semana").removeClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaMes"){
		document.getElementById("labelTipoCorte").innerHTML = "Dia del mes y hora para la realizacion del corte de turno.";
		$("#semana").addClass("hidden");
		$("#mes").removeClass("hidden");
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
    	if(valorLapso=='cadaMes'){
    		document.getElementById("labelTipoCorte").innerHTML = "Dia del mes y hora para la realizacion del corte de turno.";
        	$('#Lapso > option[value="cadaMes"]').attr('selected', 'selected');
	        $('#mes > option[value="'+valorSemana+'"]').attr('selected','selected');
	        $('#horaC').val(valorHora);
	        $('.contenedorFecha').addClass('col-md-6');
	        $('#mes').removeClass('hidden');
	        $('#semana').addClass('hidden');
	    }
	    if(valorLapso=='cadaSemana'){
	    	document.getElementById("labelTipoCorte").innerHTML = "Dia de la semana y hora para la realizacion del corte de turno.";
	        $('#Lapso > option[value="cadaSemana"]').attr('selected', 'selected');
	        $('#semana > option[value="'+valorSemana+'"]').attr('selected', 'selected');
	        $('#horaC').val(valorHora);
	        $('.contenedorFecha').addClass('col-md-6');
	        $('#semana').removeClass('hidden');
	        $('#mes').addClass('hidden');
	    }
	    if(valorLapso=='cadaDia'){
	    	document.getElementById("labelTipoCorte").innerHTML = "Hora del dia para la realización del corte de turno";
	        $('#Lapso > option[value="cadaDia"]').attr('selected', 'selected');
	        $('#horaC').val(valorHora);
	        $('.contenedorFecha').removeClass('col-md-6');        
	    }
	    if(valorLapso=='cadaDetHora'){
	    	document.getElementById("labelTipoCorte").innerHTML = "Seleccionar cada cuantas horas se realizara el corte de turno";
	        $('#Lapso > option[value="cadaDetHora"]').attr('selected', 'selected');
	        $('#horaC').val(valorHora);
	        $('.contenedorFecha').removeClass('col-md-6');            
	    }
	    if( valorLapso!=="cadaMes" && valorLapso!=="cadaSemana" && valorLapso!=="cadaDia" && valorLapso!="cadaDetHora"){$('#Lapso > option[value="cadaSemana"]').attr('selected', 'selected');
	        $('#semana > option[value="Domingo"]').attr('selected', 'selected');
	        $('#horaC').val("23:59:59");
	        $('.contenedorFecha').addClass('col-md-6');
	        $('#semana').removeClass('hidden');
	        $('#mes').addClass('hidden');   
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