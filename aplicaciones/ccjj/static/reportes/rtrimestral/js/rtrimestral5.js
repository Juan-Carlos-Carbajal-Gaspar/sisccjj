
  // Funcion De Inicio
  $(function () {

    // Cargar bootstrap 4 para buscadores de select
    $('.select2').select2({
      theme: "bootstrap4",
      language: 'es'
    });

    // Periodos de Expedientes
    var select_year = $('select[name="year"]');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'searchyear'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            // Utilizando la libreria de select2
            select_year.html('').select2({
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


    $('#btnpdf').hide();
    
    // Para Buscar Reporte Trimestral
    $('.btnSearch').on('click', function () {

      $("#data tbody tr").remove();
      
      var year=$('#year').val();
      var trimestre=$('#trimestre').val();
  
      if (year == 0 || trimestre == 0){
        message_error('Seleccione Año y Trimestre');
        return false;
      }
      else{
          
        var desde='';
        var hasta='';
  
        if (trimestre == 1){ // ENERO-MARZO
          desde=year + '-01-01';
          hasta=year + '-03-31';
        }
        else if (trimestre == 2){ // ABRIL-JUNIO
          desde=year + '-04-01';
          hasta=year + '-06-30';
        }
        else if (trimestre == 3){ // JULIO-SEPTIEMBRE
          desde=year + '-07-01';
          hasta=year + '-09-30';
        }
        else if (trimestre == 4){ // OCTUBRE-DICIEMBRE
          desde=year + '-10-01';
          hasta=year + '-12-31';
        }
        
        datosCivil(desde, hasta);

        $('#btnpdf').show();
  
      }
      
    });
  
    // Para Exportar PDF Reporte Trimestral
    $('.btnExportPDF').on('click', function () {
          
      var year=$('#year').val();
      var trimestre=$('#trimestre').val();
      var fechadesde=$('#bd-desde').val();
      var fechashasta=$('#bd-hasta').val();
      var periodo='';
  
      if (year == 0 || trimestre == 0){
        message_error('Seleccione Año y Trimestre');
        return false;
      }
      else{
  
        var desde='';
        var hasta='';
  
        if (trimestre == 1){ // ENERO-MARZO
          desde=year + '-01-01';
          hasta=year + '-03-31';
          periodo='1er TRIMESTRE';
        }
        else if (trimestre == 2){ // ABRIL-JUNIO
          desde=year + '-04-01';
          hasta=year + '-06-30';
          periodo='2do TRIMESTRE';
        }
        else if (trimestre == 3){ // JULIO-SEPTIEMBRE
          desde=year + '-07-01';
          hasta=year + '-09-30';
          periodo='3er TRIMESTRE';
        }
        else if (trimestre == 4){ // OCTUBRE-DICIEMBRE
          desde=year + '-10-01';
          hasta=year + '-12-31';
          periodo='4to TRIMESTRE';
        }
        
        window.open('/reportetrimestralpdf/' + year + '/' + periodo + '/' + fechadesde + '/' + fechashasta + '/',  '_blank');
  
      }
      
    });
  
  });



  // Para mostrar los Meses Desde Hasta
var mostrarValorMeses = function(x){
  if(x=="0"){
    document.getElementById('bd-desde').value="";
    document.getElementById('bd-hasta').value="";
  }else if(x=="1"){
    document.getElementById('bd-desde').value="ENERO";
    document.getElementById('bd-hasta').value="MARZO";
  }else if(x=="2"){
    document.getElementById('bd-desde').value="ABRIL";
    document.getElementById('bd-hasta').value="JUNIO";
  }else if(x=="3"){
    document.getElementById('bd-desde').value="JULIO";
    document.getElementById('bd-hasta').value="SEPTIEMBRE";
  }else if(x=="4"){
    document.getElementById('bd-desde').value="OCTUBRE";
    document.getElementById('bd-hasta').value="DICIEMBRE";
  }    
}

// Para mostrar datos de Materia Civil
function datosCivil(desde, hasta){
  // MATERIA CIVIL
  var trcivil = document.createElement("TR");
  trcivil.innerHTML="<tr><td colspan='12' class= 'colorblanco'><b>CIVIL</b></td></tr>";
  document.getElementById("tbody").appendChild(trcivil);
  // ----- AJAX CIVIL ----//
  $.ajax({
   url: window.location.pathname,
   type: 'POST',
   data: {
     'action': 'searchall',
     'fechdesde': desde,
     'fechhasta': hasta,
     'materia': '2'
   },
   success:  function (data) {
       for (i = 0; i < data.length; i++) {
         var tr = document.createElement('TR');
         for (j = 0; j < data[i].length; j++) {
             var td = document.createElement('TD')
             td.appendChild(document.createTextNode(data[i][j]));
             tr.appendChild(td)
         }
         document.getElementById("tbody").appendChild(tr);
       }

       // Totalidades de MATERIA CIVIL
       // ----- AJAX CIVIL TOTALIDADES----//
        $.ajax({
          url: window.location.pathname,
          type: 'POST',
          data: {
            'action': 'searchallmateria',
            'fechdesde': desde,
            'fechhasta': hasta,
            'materia': '2'
          },
          success:  function (data) {
              for (i = 0; i < data.length; i++) {
                var tr = document.createElement('TR');
                for (j = 0; j < data[i].length; j++) {
                    var td = document.createElement('TD')
                    td.appendChild(document.createTextNode(data[i][j]));
                    tr.appendChild(td)
                }
                document.getElementById("tbody").appendChild(tr);
              }      
              datosFamilia(desde, hasta);    
          }
        });
        // ----- AJAX CIVIL TOTALIDADES ----//
       
       // Totalidades de MATERIA CIVIL

      //  datosFamilia(desde, hasta);    
   }
  });
  // ----- AJAX CIVIL ----//
}

// Para mostrar datos de Materia Familia
function datosFamilia(desde, hasta){
  // MATERIA FAMILIA
  var trfamilia = document.createElement("TR");
  trfamilia.innerHTML="<tr><td colspan='12' class= 'colorblanco'><b>FAMILIA</b></td></tr>";
  document.getElementById("tbody").appendChild(trfamilia);
  // ----- AJAX FAMILIA ----//
  $.ajax({
    url: window.location.pathname,
    type: 'POST',
    data: {
      'action': 'searchall',
      'fechdesde': desde,
      'fechhasta': hasta,
      'materia': '1'
    },
    success:  function (data) {
      for (i = 0; i < data.length; i++) {
        var tr = document.createElement('TR');
        for (j = 0; j < data[i].length; j++) {
          var td = document.createElement('TD')
          td.appendChild(document.createTextNode(data[i][j]));
          tr.appendChild(td)
        }
        document.getElementById("tbody").appendChild(tr); 
      }
      // Totalidades de MATERIA FAMILIA
       // ----- AJAX CIVIL FAMILIA----//
       $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
          'action': 'searchallmateria',
          'fechdesde': desde,
          'fechhasta': hasta,
          'materia': '1'
        },
        success:  function (data) {
            for (i = 0; i < data.length; i++) {
              var tr = document.createElement('TR');
              for (j = 0; j < data[i].length; j++) {
                  var td = document.createElement('TD')
                  td.appendChild(document.createTextNode(data[i][j]));
                  tr.appendChild(td)
              }
              document.getElementById("tbody").appendChild(tr);
            }      
            datosContratacionesEstado(desde, hasta);    
        }
      });
      // ----- AJAX FAMILIA TOTALIDADES ----//
     
     // Totalidades de MATERIA FAMILIA

      
    }
  });
  // ----- AJAX FAMILIA ----//     
}

// Para mostrar datos de Materia Contrataciones Con el Estado
function datosContratacionesEstado(desde, hasta){
  // MATERIA CONTRATACIONES CON EL ESTADO
  var trcontrataciones = document.createElement("TR");
  trcontrataciones.innerHTML="<tr><td colspan='12' class= 'colorblanco'><b>CONTRATACIONES CON EL ESTADO</b></td></tr>";
  document.getElementById("tbody").appendChild(trcontrataciones);
  // ----- AJAX CONTRATACIONES CON EL ESTADO ----//
  $.ajax({
    url: window.location.pathname,
    type: 'POST',
    data: {
      'action': 'searchall',
      'fechdesde': desde,
      'fechhasta': hasta,
      'materia': '3'
    },
    success:  function (data) {
        for (i = 0; i < data.length; i++) {
          var tr = document.createElement('TR');
          for (j = 0; j < data[i].length; j++) {
              var td = document.createElement('TD')
              td.appendChild(document.createTextNode(data[i][j]));
              tr.appendChild(td)
          }
          document.getElementById("tbody").appendChild(tr);
        }
        // Totalidades de MATERIA CONTRATACIONES CON EL ESTADO
       // ----- AJAX CIVIL CONTRATACIONES CON EL ESTADO----//
       $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
          'action': 'searchallmateria',
          'fechdesde': desde,
          'fechhasta': hasta,
          'materia': '3'
        },
        success:  function (data) {
            for (i = 0; i < data.length; i++) {
              var tr = document.createElement('TR');
              for (j = 0; j < data[i].length; j++) {
                  var td = document.createElement('TD')
                  td.appendChild(document.createTextNode(data[i][j]));
                  tr.appendChild(td)
              }
              document.getElementById("tbody").appendChild(tr);
            }
            // ESPACIO PARA TOTAL GENERAL
            var trespacio = document.createElement("TR");
            trespacio.innerHTML="<tr><td colspan='12' class= 'colorblanco'>&nbsp;</td></tr>";
            document.getElementById("tbody").appendChild(trespacio);
            // ----- AJAX TOTAL GENERAL----//
            $.ajax({
              url: window.location.pathname,
              type: 'POST',
              data: {
                'action': 'searchallgeneral',
                'fechdesde': desde,
                'fechhasta': hasta
              },
              success:  function (data) {
                  for (i = 0; i < data.length; i++) {
                    var tr = document.createElement('TR');
                    for (j = 0; j < data[i].length; j++) {
                        var td = document.createElement('TD')
                        td.appendChild(document.createTextNode(data[i][j]));
                        tr.appendChild(td)
                    }
                    document.getElementById("tbody").appendChild(tr);
                  }
                  
              }
            });
            // ----- AJAX TOTAL GENERAL ----//
        }
      });
      // ----- AJAX CONTRATACIONES CON EL ESTADO TOTALIDADES ----//
     
     // Totalidades de CONTRATACIONES CON EL ESTADO
      }
  });
  // ----- AJAX CONTRATACIONES CON EL ESTADO ----//     
}
  
  
  
  
  