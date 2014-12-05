/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
$('#modalTarifa').on('shown.bs.modal', function () {
	$('#nuevaTarifa').val("");
    $('#nuevaTarifa').focus();
})

$('#modalAcceso').on('shown.bs.modal', function () {
    $('#nuevoTiempo').val("");
    $('#nuevoTiempo').focus();
})


/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
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


/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
$("#ReportesAceptar").click(function(){
	if($("#valorticket").val()==0 && $("#valorturno").val()==0 && $("#valorfecha").val()==0 && $("#valortarifa").val()==0 && $("#valortotal").val()==0){
		$("#MensajeReportes").addClass("hidden");
		$("#MensajeReportes").removeClass("hidden");
	return false;
	}
});


/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
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


/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
$(".close").click(function(){
	$(".contentAlerttas").addClass("hidden");
});

$("#cerrarAlertaLogin").click(function(){
	$("#contenidoLogin").removeClass("errorLogin");
});



/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
$("#enviarConfiguracion").click(function(){
	var numerosValidacion=$("#numeroMedida").val();
	if(!/^[0-9]{1,4}?$/.test(numerosValidacion)){
		document.getElementById('textoAlerta').innerHTML="Los valores introducidos no están dentro del rango válido";
		$("article.mensajesPassword").show();
		$("#numeroMedida").val("");
		return false;
	}
});


/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
$("#cambioConfiguracion").mouseover(function(){
	valorRadio=$('input:radio[name=valor]:checked').val();
	$("#cambiarCorte").val(valorRadio);
});


/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
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


/*
     @method
     Indicates that the block describes a method for the current class.
     @description
     The method description.
     @param
     Defines a parameter for an ordinary @method.
     @return
     Specifies a method's return value.
*/
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