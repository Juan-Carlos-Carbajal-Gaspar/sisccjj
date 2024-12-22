$(function () {
    /* ChartJS
     * -------
     * Here we will create a few charts using ChartJS
     */
    // Buscar Periodo 
    var select_periodo = $('select[name="periodo"]');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'searchperiodo'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            // Utilizando la libreria de select2
            select_periodo.html('').select2({
                theme: "bootstrap4",
                language: "es",
                data: data
            });
            
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
        //select_procedimientos.html(options);
    });
})

function mostrarChart(){
  var periodoyear=document.getElementById("periodo").value;

  if(periodoyear == "0"){
    alert("Seleccione bien el periodo");
  }else{
    $.ajax({
      url:   window.location.pathname,
      method: 'POST',
      data:  {
        'action': 'datapago',
        'year': periodoyear
      },
      success: function(data)            
      {
        // console.log(JSON.stringify(data));
        dibujarChart(data,'line', "lineChart");
        dibujarChart(data,'bar', "barChart");         
      }
    });
  }
}

function dibujarChart(datareporte,tipografico, graficomostrar){
            
  var ctx = $('#' + graficomostrar).get(0).getContext('2d')
  var areaChartData = { 
    labels  : ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    
    datasets: [
      {
        label               : 'Ingresos',
        backgroundColor     : 'blue',
        borderColor         : 'blue',
        pointRadius          : false,
        pointColor          : 'blue',
        pointStrokeColor    : 'rgba(60,141,188,1)',
        pointHighlightFill  : '#fff',
        pointHighlightStroke: 'rgba(60,141,188,1)',
        data: datareporte.ingresos
      },
      {
        label               : 'Egresos',
        backgroundColor     : 'red',
        borderColor         : 'red',
        pointRadius         : false,
        pointColor          : 'red',
        pointStrokeColor    : '#c1c7d1',
        pointHighlightFill  : '#fff',
        pointHighlightStroke: 'rgba(220,220,220,1)',
        data: datareporte.egresos
      },
      
    ]
  }

  var areaChartOptions = {
    maintainAspectRatio : false,
    responsive : true,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines : {
          display : false,
        }
      }],
      yAxes: [{
        gridLines : {
          display : false,
        }
      }]
    }
  }

  if (tipografico == 'line'){
    var lineChartOptions = $.extend(true, {}, areaChartOptions)
    var lineChartData = $.extend(true, {}, areaChartData)
    lineChartData.datasets[0].fill = false;
    lineChartData.datasets[1].fill = false;
    lineChartOptions.datasetFill = false

    new Chart(ctx, {
      type: tipografico,
      data: lineChartData,
      options: lineChartOptions
    })
  }
  else if (tipografico == 'bar'){
    var barChartData = $.extend(true, {}, areaChartData)
    var temp0 = areaChartData.datasets[0]
    var temp1 = areaChartData.datasets[1]
    barChartData.datasets[1] = temp1
    barChartData.datasets[0] = temp0

    var barChartOptions = {
      responsive              : true,
      maintainAspectRatio     : false,
      datasetFill             : false
    }

    new Chart(ctx, {
      type: tipografico,
      data: barChartData,
      options: barChartOptions
    })
  }
}