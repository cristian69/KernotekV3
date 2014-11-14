
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
	if(nombreVentana=="UsuarioInvalido"){
		$("#contenidoLogin").addClass("errorLogin");
	}
}

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
		document.getElementById('textoAlerta').innerHTML="Los valores introducidos no estan dentro del rango válido";
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


function graficaDias(labelDias, datosDias){
	$("#diaria").addClass("active");
	$("#graficaenDias").addClass("active");
	$("#semanal").removeClass("active");
	$("#graficaenSemanas").removeClass("active");
	$("#mensual").removeClass("active");
<<<<<<< HEAD
	$("#graficaenMeses").removeClass("active");	
var lineChartData1 = {
			labels : [labelDias[0],labelDias[1],labelDias[2],labelDias[3],labelDias[4],labelDias[5],labelDias[6]],
			datasets : [
				{
					label: "Primera serie de datos",
					fillColor : "rgba(220,220,220,0.2)",
					strokeColor : "#009DE0",
					pointColor : "rgba(151,187,205,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(0,247,247,1)",
					data : [datosDias[0],datosDias[1],datosDias[2],datosDias[3],datosDias[4],datosDias[5],datosDias[6]]
				}
			]

		}
		var ctx1 = document.getElementById("graficaDia").getContext("2d");
		window.myPie = new Chart(ctx1).Line(lineChartData1, {responsive:true});
		
	}

function graficaSemanas(labelSemanas, datosSemanas){		
		$("#diaria").removeClass("active");
		$("#graficaenDias").removeClass("active");
		$("#semanal").addClass("active");
		$("#graficaenSemanas").addClass("active");
		$("#mensual").removeClass("active");
		$("#graficaenMeses").removeClass("active");
		var lineChartData2 = {
			labels : [labelSemanas[0], labelSemanas[1], labelSemanas[2], labelSemanas[3], labelSemanas[4], labelSemanas[5], labelSemanas[6]],
			datasets : [
				{
					label: "Primera serie de datos",
					fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "#009DE0",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
					data : [datosSemanas[0], datosSemanas[1], datosSemanas[2], datosSemanas[3], datosSemanas[4], datosSemanas[5], datosSemanas[6]]
				}
			]
=======
	$("#graficaenMeses").removeClass("active");
	var lineChartData1 = {
		labels : [labelDias[0],labelDias[1],labelDias[2],labelDias[3],labelDias[4],labelDias[5],labelDias[6]],
		datasets :
		{
			label: "Primera serie de datos",
			fillColor : "rgba(220,220,220,0.2)",
			strokeColor : "#6b9dfa",
			pointColor : "#1e45d7",
			pointStrokeColor : "#fff",
			pointHighlightFill : "#fff",
			pointHighlightStroke : "rgba(220,220,220,1)",
			data : [datosDias[0],datosDias[1],datosDias[2],datosDias[3],datosDias[4],datosDias[5],datosDias[6]]
		}
		]
	}
	var ctx4 = document.getElementById("graficaDia").getContext("2d");
	window.myPie = new Chart(ctx4).Line(lineChartData1, {responsive:true});
}


>>>>>>> e4eada0be3a4bba413df802ea35f47f5443a329e

function graficaSemanas(labelSemanas, datosSemanas){
	$("#diaria").removeClass("active");
	$("#graficaenDias").removeClass("active");
	$("#semanal").addClass("active");
	$("#graficaenSemanas").addClass("active");
	$("#mensual").removeClass("active");
	$("#graficaenMeses").removeClass("active");
	var lineChartData2 = {
		labels : [labelSemanas[0], labelSemanas[1], labelSemanas[2], labelSemanas[3], labelSemanas[4], labelSemanas[5], labelSemanas[6]],
		datasets : [
		{
			label: "Primera serie de datos",
			fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "#009DE0",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
			data : [datosSemanas[0], datosSemanas[1], datosSemanas[2], datosSemanas[3], datosSemanas[4], datosSemanas[5], datosSemanas[6]]
		}
<<<<<<< HEAD
		var ctx2 = document.getElementById("graficaSemana").getContext("2d");
		window.myPie = new Chart(ctx2).Line(lineChartData2, {responsive:true});
	}

function graficaMeses(labelMeses, datosMeses){
	$("#diaria").removeClass("active");
	$("#graficaenDias").removeClass("active");
	$("#semanal").removeClass("active");
	$("#graficaenSemanas").removeClass("active");
	$("#mensual").addClass("active");
	$("#graficaenMeses").addClass("active");
		var lineChartData3 = {
			labels : [labelMeses[0], labelMeses[1], labelMeses[2], labelMeses[3], labelMeses[4], labelMeses[5], labelMeses[6]],
			datasets : [
				{
					label: "Primera serie de datos",
					fillColor: "rgba(220,220,220,0.2)",
		            strokeColor: "#009DE0",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(220,220,220,1)",
					data : [datosMeses[0], datosMeses[1], datosMeses[2], datosMeses[3], datosMeses[4], datosMeses[5], datosMeses[6]]
				}
			]
=======
		]
	}
	var ctx2 = document.getElementById("graficaSemana").getContext("2d");
	window.myPie = new Chart(ctx2).Line(lineChartData2, {responsive: true});
}
>>>>>>> e4eada0be3a4bba413df802ea35f47f5443a329e

function graficaMeses(labelMeses, datosMeses){
	$("#diaria").removeClass("active");
	$("#graficaenDias").removeClass("active");
	$("#semanal").removeClass("active");
	$("#graficaenSemanas").removeClass("active");
	$("#mensual").addClass("active");
	$("#graficaenMeses").addClass("active");
	var lineChartData3 = {
		labels : [labelMeses[0], labelMeses[1], labelMeses[2], labelMeses[3], labelMeses[4], labelMeses[5], labelMeses[6]],
		datasets : [
		{
			label: "Primera serie de datos",
			fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "#009DE0",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
			data : [datosMeses[0], datosMeses[1], datosMeses[2], datosMeses[3], datosMeses[4], datosMeses[5], datosMeses[6]]
		}
<<<<<<< HEAD
		var ctx3 = document.getElementById("graficaMes").getContext("2d");
		window.myPie = new Chart(ctx3).Line(lineChartData3, {responsive:true});
=======
		]
>>>>>>> e4eada0be3a4bba413df802ea35f47f5443a329e
	}
	var ctx3 = document.getElementById("graficaMes").getContext("2d");
	window.myPie = new Chart(ctx3).Line(lineChartData3, {responsive: true});
}
