var tblCliente;
function getData(){
      tblCliente=$('#data').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        // buttons: [ 'excel', 'pdf'],
        // dom: 'Blfrtip',
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'listacliente'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "per.numdoc_per"},
            {"data": "per.nom_per"},
            {"data": "per.eda_per"},
            {"data": "per.sex_per.name"},
            {"data": "per.dir_per"},
            {"data": "per.numcel_per"},
            {"data": "per.ema_per"},
            {"data": "id"},
            
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a href="/cliente/editarcliente/' + row.per.id +'/" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return row.per.nom_per + ' ' + row.per.apepat_per + ' ' + row.per.apemat_per
                }
            },
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
  }

$(function () {
    // Para validar Numero de DNi
    $('input[name="numdoc_per"]').bind('keypress', function(event) {
        var regex = new RegExp("^[0-9]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
            event.preventDefault();
            return false;
        }
    });

    // Para validar Edad
    $('input[name="eda_per"]').bind('keypress', function(event) {
        var regex = new RegExp("^[0-9]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
            event.preventDefault();
            return false;
        }
    });


    // Para validar Numero de celular
    $('input[name="numcel_per"]').bind('keypress', function(event) {
        var regex = new RegExp("^[0-9]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
          event.preventDefault();
          return false;
        }
    });
   
    // Para Cargar los datos a la tabla
    getData();

});
  
  