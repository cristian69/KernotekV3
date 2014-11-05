
$("#fechasReporte").click(function(){
	if($("#fecha_fin").val() == "" || $("#fecha_inicio").val() == "" || $("#hora_fin").val() == "" || $("#hora_inicio").val() == 
		""){
		$("#errorFechas").removeClass("hidden");
	}
	else{
		$("#reportepaso1").removeClass('active');
		$("#reportetab1").removeClass('active');
		$("#reportepaso2").addClass('active');
		$("#reportetab2").addClass('active');
		document.getElementById('btnReportes').innerHTML="<li><button type='button' class='btn' id='anteriorReporte'>Anterior</button></li><p><><li><button type='button' class='btn' id='siguienteReporte'>Siguiente</button></li>";
	}
});


$(".ocultarApartado").click(function(){
	$(".editarLlave").addClass("hidden");
	$(".informacionUsuario").addClass("hidden");
	$(".tablaLlaves").removeClass("hidden");
});

$("#buscarTurnos").click(function(){
	if($("#fecha_inicio").val()==""){
		alert("El campo de Fecha de Inicio es Requerido");
		return false;
	}
});

function redireccionar(valor, direccion){
	if(valor=='si'){
		setTimeout(function(){
			window.location.href=direccion;
		},30);
	}
}




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
	alert(sa);
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


function graficas(){
		var lineChartData2 = {
			labels : ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"],
			datasets : [
				{
					label: "Primera serie de datos",
					fillColor : "rgba(220,220,220,0.2)",
					strokeColor : "#6b9dfa",
					pointColor : "#1e45d7",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(220,220,220,1)",
					data : [90,30,10,80,15,5,15]
				}
			]

		}
		var lineChartData3 = {
			labels : ["Semana 1","Semana 2","Semana 3","Semana 4"],
			datasets : [
				{
					label: "Primera serie de datos",
					fillColor : "rgba(220,220,220,0.2)",
					strokeColor : "#6b9dfa",
					pointColor : "#1e45d7",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(220,220,220,1)",
					data : [90,30,10,80]
				}
			]

		}
		var lineChartData1 = {
			labels : ["1","2","3","4","5","6","7" ,"8" ,"9" ,"10" ,"11", "12","13" ,"14" ,"15" ,"16" ,"17" ,"18" ,"19" ,"20", "21", "22", "23", "24"],
			datasets : [
				{
					label: "Primera serie de datos",
					fillColor : "rgba(220,220,220,0.2)",
					strokeColor : "#6b9dfa",
					pointColor : "#1e45d7",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(220,220,220,1)",
					data : [150,300,100,800,150,50,150,123, 145, 167, 177, 199, 199, 112, 111, 100, 200, 500, 300, 300, 100, 105, 300, 400,]
				}
			]

		}
		var ctx1 = document.getElementById("graficaDia").getContext("2d");
		window.myPie = new Chart(ctx1).Line(lineChartData1);
		var ctx2 = document.getElementById("graficaSemana").getContext("2d");
		window.myPie = new Chart(ctx2).Line(lineChartData2);
		var ctx3 = document.getElementById("graficaMes").getContext("2d");
		window.myPie = new Chart(ctx3).Line(lineChartData3);
	}