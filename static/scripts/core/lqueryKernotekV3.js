function home(){
	$("#accionRealizar").select2({
		placeholder:"Tipo de reporte"
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




function validarNumeros(){
	numeroValidar=$("#nTarifa").val();
	if(!/^[0-9]{1,5}(\.[0-9]{0,2})?$/.test(numeroValidar) || !/^[0-9]{1,3}$/.test(numeroValidar)){
		$("#errorFormato").removeClass("display-none");
		$("#"+valorId).val()="";
	}
	else{
		$("#errorFormato").addClass("display-none");
		$("#paso2").addClass("active");
		$("#paso1").removeClass("active");
		$("#tab2").addClass("active");
		$("#tab1").removeClass("active");
	document.getElementById("btnTarifa").innerHTML="<li><button type='button'class='btn' onclick='regresarTarifa();'>Regresar</button><button type='submit' class='btn blue' name='submit'>Aceptar</button></li>"
	}
}

