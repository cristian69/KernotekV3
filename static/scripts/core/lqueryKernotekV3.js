function home(){
	$("#accionRealizar").select2({
		placeholder:"Tipo de reporte"
	});
	$("#Lapso").select2();
	$("#semana").select2();
	$("#mes").select2();
	$("#tiposCortes").select2({
		placeholder: "Selecciona el tipo de dorte de turno"
	});
	$("#seleccionarAccion").select2({
		placeholder:"seleccionar acción"
	});
	$('input').iCheck({
		checkboxClass: 'icheckbox_square-blue',
		radioClass: 'iradio_square-blue',
		increaseArea: '80%'
	});
}




$("#siguienteReporte").click(function(){
	if($("#tipoReporte").val()=="fechas"){
		$("#reportetab2").addClass("active");
		$("#reportepaso2").addClass("active");
		$("#reportetab1").removeClass("active");
		$("#reportepaso1").removeClass("active");
		$("#reportepaso2 .step").removeClass("hidden");
		$("#aceptarReporte").removeClass("hidden");
		$("#anteriorReporte").removeClass("hidden");
		$("#siguienteReporte").addClass("hidden");
	}
	if($("#tipoReporte").val()=="turno"){
		$("#reportetab2").addClass("active");
		$("#reportepaso2").addClass("active");
		$("#reportetab1").removeClass("active");
		$("#reportepaso1").removeClass("active");
		$("#reportepaso2 .step").removeClass("hidden");
		$("#reportepaso3 .step").removeClass("hidden");
		$("#anteriorReporte").removeClass("hidden");
	}
});

$("#anteriorReporte").click(function(){
	$("#reportetab2").removeClass("active");
	$("#reportepaso2").removeClass("active");
	$("#reportetab1").addClass("active");
	$("#reportepaso1").addClass("active");
	$("#reportepaso2 .step").addClass("hidden");
	$("#reportepaso3 .step").addClass("hidden");
	$("#aceptarReporte").addClass("hidden");
	$("#anteriorReporte").addClass("hidden");
	$("#siguienteReporte").removeClass("hidden");
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

$("#siguienteCorte").click(function(){
	if($("#seleccionarAccion").val()=="corte"){
		$("#AceptarCorte").removeClass("hidden");
		$("#CancelarCorte").removeClass("hidden");
		$("#siguienteCorte").addClass("hidden");
		$("#pasoTurno2b .step").removeClass("hidden");
		$("#pasoTurno2b").addClass("active");
		$("#pasoTurno1").removeClass("active");
		$("#Turno1").removeClass("active");
		$("#Turno2b").addClass("active");

	}
	if($("#seleccionarAccion").val()=="configurar"){
		$("#pasoTurno2").addClass("active");
		$("#pasoTurno1").removeClass("active");
		$("#turno2").addClass("active");
		$("#Turno1").removeClass("active");
		$("#pasoTurno2 .step").removeClass("hidden");
		$("#anteriorCorte").removeClass("hidden");
		$("#ConfirmarAccion").removeClass("hidden");
		$("#siguienteCorte").addClass("hidden");
	}
	if($("#seleccionarAccion").val()=="cambiar" && $("#valorPestaña").val()=="1"){
		$("#pasoTurno2a").addClass("active");
		$("#pasoTurno2a .step").removeClass("hidden");
		$("#Turno2a").addClass("active");
		$("#pasoTurno1").removeClass("active");
		$("#Turno1").removeClass("active");	
		$("#anteriorCorte").removeClass("hidden");
		$("#valorPestaña").val("2");	
	}
	if($("#seleccionarAccion").val()=="cambiar" && $("#tiposCortes").val()=="automatico"){
		$("#pasoTurno2a").removeClass("active");
		$("#Turno2a").removeClass("active");		
		$("#pasoTurno3a").addClass("active");
		$("#pasoTurno3a .step").removeClass("hidden");
		$("#turno2").addClass("active");
		$("#siguienteCorte").addClass("hidden");
		$("#ConfirmarAccion").removeClass("hidden");
		$("#valorPestaña").val("3");
	}
	
});

$("#CancelarCorte").click(function(){
	if($("#seleccionarAccion").val()=="corte"){
		$("#AceptarCorte").addClass("hidden");
		$("#CancelarCorte").addClass("hidden");
		$("#siguienteCorte").removeClass("hidden");
		$("#pasoTurno2b .step").addClass("hidden");
		$("#pasoTurno2b").removeClass("active");
		$("#pasoTurno1").addClass("active");
		$("#Turno1").addClass("active");
		$("#Turno2b").removeClass("active");
	}
});

$("#anteriorCorte").click(function(){
	if($("#seleccionarAccion").val()=="configurar"){
		$("#pasoTurno2").removeClass("active");
		$("#pasoTurno1").addClass("active");
		$("#turno2").removeClass("active");
		$("#Turno1").addClass("active");
		$("#pasoTurno2 .step").addClass("hidden");
		$("#anteriorCorte").addClass("hidden");
		$("#ConfirmarAccion").addClass("hidden");
		$("#siguienteCorte").removeClass("hidden");
	}
	if($("#seleccionarAccion").val()=="cambiar" && $("#valorPestaña").val()=="2"){
		$("#pasoTurno2a").removeClass("active");
		$("#pasoTurno2a .step").addClass("hidden");
		$("#Turno2a").removeClass("active");
		$("#pasoTurno1").addClass("active");
		$("#Turno1").addClass("active");	
		$("#anteriorCorte").addClass("hidden");
		$("#siguienteCorte").removeClass("hidden");
		$('#tiposCortes > option[value=""]').attr('selected', 'selected');
		$("#valorPestaña").val("1");	
	}	
	if($("#seleccionarAccion").val()=="cambiar" && $("#valorPestaña").val()=="3"){
		$("#pasoTurno2a").addClass("active");
		$("#Turno2a").addClass("active");		
		$("#pasoTurno3a").removeClass("active");
		$("#pasoTurno3a .step").addClass("hidden");
		$("#turno2").removeClass("active");
		$("#siguienteCorte").removeClass("hidden");
		$("#anteriorCorte").removeClass("hidden");
		$("#ConfirmarAccion").addClass("hidden");
		$("#valorPestaña").val("2");
	}	

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
	if($("#tiposCortes").val()=="manual"){
		$("#ConfirmarAccion").removeClass("hidden");
		$("#siguienteCorte").addClass("hidden");
	}
	else{
		$("#ConfirmarAccion").addClass("hidden");
		$("#siguienteCorte").removeClass("hidden");
	}
});


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
		if($("#seleccionarAccion").val()=="corte"){
			$("#aceptarAccion").removeClass("hidden");
			$("#cancelarAccion").removeClass("hidden");
			$("#nextTurno").addClass("hidden");
			$("#mturno2").addClass("active");
			$("#paso2").addClass("active");
			$("#mturno1").removeClass("active");
			$("#paso1").removeClass("active");
			$("#paso2").removeClass("hidden");
		}
		if($("#seleccionarAccion").val()=="configurar"){
			$("#paso4").removeClass("hidden");
			$("#paso4").addClass("active");
			$("#mturno4").addClass("active");
			$("#mturno1").removeClass("active");
			$("#paso1").removeClass("active");
			$("#aceptarAccion").removeClass("hidden");
			$("#cancelarAccion").removeClass("hidden");
			$("#nextTurno").addClass("hidden");
		}
		if($("#seleccionarAccion").val()=="cambiar"){
			$("#paso3").addClass("active");
			$("#paso3").removeClass("hidden");
			$("#mturno3").addClass("active");
			$("#paso1").removeClass("active");
			$("#mturno1").removeClass("active");
			$("#backTurno").removeClass("hidden");
			$("#banderaPosicion").val("2");
		}

		if($("#seleccionarAccion").val()=="cambiar" && $("#tiposCortes").val()=="automatico"){
			$("#paso3").removeClass("active");
			$("#mturno3").removeClass("active");
			$("#paso4").addClass("active");
			$("#paso4").removeClass("hidden");
			$("#mturno4").addClass("active");
			$("#nextTurno").addClass("hidden");
			$("#aceptarAccion").removeClass("hidden");
			$("#banderaPosicion").val("3");
		}
	});






	/*Cancelar el corte manual*/
	$("#cancelarAccion").click(function(){
		if($("#seleccionarAccion").val()=="corte"){
			$("#aceptarAccion").addClass("hidden");
			$("#cancelarAccion").addClass("hidden");
			$("#nextTurno").removeClass("hidden");
			$("#mturno2").removeClass("active");
			$("#paso2").removeClass("active");
			$("#mturno1").addClass("active");
			$("#paso1").addClass("active");
			$("#paso2").addClass("hidden");
		}
		if($("#seleccionarAccion").val()=="configurar"){
			$("#paso4").addClass("hidden");
			$("#paso4").removeClass("active");
			$("#mturno4").removeClass("active");
			$("#mturno1").addClass("active");
			$("#paso1").addClass("active");
			$("#aceptarAccion").addClass("hidden");
			$("#cancelarAccion").addClass("hidden");
			$("#nextTurno").removeClass("hidden");	
		}
	});


	$("#backTurno").click(function(){
		if($("#seleccionarAccion").val()=="cambiar" && $("#banderaPosicion").val()=="2"){
			$("#paso3").removeClass("active");
			$("#paso3").addClass("hidden");
			$("#mturno3").removeClass("active");
			$("#mturno3").removeClass("active");
			$("#paso1").addClass("active");
			$("#mturno1").addClass("active");
			$("#backTurno").addClass("hidden");
			$("#banderaPosicion").val("1")
		}
		if($("#seleccionarAccion").val()=="cambiar" && $("#tiposCortes").val()=="automatico" && $("#banderaPosicion").val()!="1"){
			$("#paso3").addClass("active");
			$("#mturno3").addClass("active");
			$("#paso4").removeClass("active");
			$("#paso4").addClass("hidden");
			$("#mturno4").removeClass("active");
			$("#nextTurno").removeClass("hidden");
			$("#aceptarAccion").addClass("hidden");
			$('#tiposCortes > option[value=""]').attr('selected', 'selected');
			$("#banderaPosicion").val("2");
		}

		
	});