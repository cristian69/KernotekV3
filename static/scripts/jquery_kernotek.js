$('#modalTarifa').on('shown.bs.modal', function () {
    $('#nuevaTarifa').val("");
    $('#nuevaTarifa').focus();
})
$('#modalAcceso').on('shown.bs.modal', function () {
    $('#nuevoTiempo').val("");
    $('#nuevoTiempo').focus();
})


$("#configCorte").mouseover(function(){
	if($("#Lapso").val()!="cadaSemana" && $("#Lapso").val()!="cadaMes"){
		$("#semana").addClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").removeClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaSemana"){
		$("#semana").removeClass("hidden");
		$("#mes").addClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
	if($("#Lapso").val()=="cadaMes"){
		$("#semana").addClass("hidden");
		$("#mes").removeClass("hidden");
		$(".contenedorFecha").addClass("col-md-6");
	}
});




$("#ReportesAceptar").click(function(){
	if($("#valorticket").val()==0 && $("#valorturno").val()==0 && $("#valorfecha").val()==0 && $("#valortarifa").val()==0 && $("#valortotal").val()==0){
		$("#MensajeReportes").addClass("hidden");
		$("#MensajeReportes").removeClass("hidden");
	return false;
	}
});



function reporteTurno(sa){
	$("#valorTurno").select2();
}



function tipoReporte(){
	$("#tipoReporte").select2({
		placeholder:"Tipo de reporte"
	});
}

function llavesSistema(){
	$("#estadoLlave").select2({
		placeholder: "Estado llave"
	});
	$("#tipoLlave").select2({
		placeholder: "Tipo De Llave"
	});
}




function mostrarVentanas(parametro){
	this.nombreVentana=parametro;
	$("#"+nombreVentana).removeClass("hidden");
	if(parametro!=""){
		$(".contentAlerttas").removeClass("hidden");
	}
	if(nombreVentana=="UsuarioInvalido"){
		$("#contenidoLogin").addClass("errorLogin");
	}
}
$(".close").click(function(){
	$(".contentAlerttas").addClass("hidden");
});

$("#cerrarAlertaLogin").click(function(){
	$("#contenidoLogin").removeClass("errorLogin");
});


function corteActual(entrada){
	this.estado=entrada;
	$("#tipoDate").select2();
	$("#Lapso").select2();
	$("#mes").select2();
	$("#semana").select2();
	if(estado=='manual'){
		$("#hacerCorte").removeClass("hidden");
		$("#cambiarCorte").val('0');
		$(".valorCorte").val('0');
	}
	if(estado=='automatico'){
		$("#cambiarCorte").val('1');
		$("#configurarCorte").removeClass("hidden");
		$(".valorCorte").val('1');
		$("#izquierdo").removeClass("col-md-3");
		$("#derecho").removeClass("col-md-3");		
	}
}



$("#enviarConfiguracion").click(function(){
	var numerosValidacion=$("#numeroMedida").val();
	if(!/^[0-9]{1,4}?$/.test(numerosValidacion)){
		document.getElementById('textoAlerta').innerHTML="Los valores introducidos no están dentro del rango válido";
		$("article.mensajesPassword").show();
		$("#numeroMedida").val("");
		return false;
	}
});


$("#cambioConfiguracion").mouseover(function(){
	valorRadio=$('input:radio[name=valor]:checked').val();
	$("#cambiarCorte").val(valorRadio);
});

$("#cambiarCortetuerno").click(function(){
	if($("#valor1").attr("checked")){
		$("#cambiarCorteturno").modal("show");
	}
	if($(".valorCorte").val()==0 && $("#valor2").attr("checked")){
		$("#configurarCorte").removeClass("hidden");
		$("#izquierdo").removeClass("col-md-3");
		$("#derecho").removeClass("col-md-3");
		$("#configTurno").addClass("hidden");
		$("#valor1").prop("disabled",true);
	}
});


function cambiarEstado(parametro){
	this.respuesta=parametro;
	if(respuesta=='cambioTipo'){
		$(".thead1").addClass("hidden");
		$("#hacerCorte").addClass("hidden");
		$("#configTurno").removeClass("hidden");
		$("#seleccionTurno").removeClass("hidden");
		$("#enlaceConfigurar").addClass("hidden");
	}
	if(respuesta=='configAutomatico'){
	$(".tituloCambioConfig").removeClass('hidden');
	$(".tituloConfigActual").addClass('hidden');
	$(".lblIngresarValores").removeClass('hidden');
	$("#Lapso").removeAttr('disabled');
	$("#semana").removeAttr('disabled');
	$("#mes").removeAttr('disabled');
	$("#horaC").removeAttr('disabled');	
	$("#configAutomatico").addClass('hidden');
	$(".btnConfigurar").removeClass('hidden');	
	}
	if(respuesta=="cancelar"){
		window.location.reload(true);
	}

}

function graficasHome(parametro, labels, datos){
	if(parametro=="graficaDia"){
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
	if(parametro=="graficaSemana"){
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
	if(parametro=="graficaMes"){
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