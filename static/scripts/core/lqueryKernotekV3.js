function home(){
	$("#accionRealizar").select2({
		placeholder:"Tipo de reporte"
	});
}

function wizardTarifa(){
	opcipon=$("#accionRealizar").val();
	if(opcipon=="tarifa"){
		$("#tarifaPaso2").removeClass("hidden");
		$("#tarifaPaso2").addClass("active");
		$("#tarifaPaso1").removeClass("active");
		$("#tarifaPaso1").addClass("correcto");
		$("#tarifaPaso3").addClass("hidden");
		$("#tarifa1").removeClass("active");
		$("#tarifa2").addClass("active");
		$("#tarifa3").removeClass("active");
		$("#aceptarTarifa").removeClass("hidden");
		$("#anteriorTarifa").removeClass("hidden");
		$("#siguienteTarifa").addClass("hidden");
	}
	if(opcipon=="corte"){
		$("#tarifaPaso3").removeClass("hidden");
		$("#tarifaPaso3").addClass("active");
		$("#tarifaPaso1").removeClass("active");
		$("#tarifaPaso2").addClass("hidden");
		$("#tarifa1").removeClass("active");
		$("#tarifa3").addClass("active");
		$("#tarifa3").removeClass("active");
		$("#aceptarTarifa").removeClass("hidden");
		$("#anteriorTarifa").removeClass("hidden");
		$("#siguienteTarifa").addClass("hidden");
	}
}










function regresarTarifa(){
	$("#paso2").removeClass("active");
	$("#paso1").addClass("active");
	$("#tab2").removeClass("active");
	$("#tab1").addClass("active");
	document.getElementById("btnTarifa").innerHTML="<li><button type='button' class='btn' onclick='validarNumeros();'>Siguiente</button></li>"
}

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

