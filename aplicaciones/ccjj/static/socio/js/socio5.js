var tblSocio;
function getData(){
      tblSocio=$('#data').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'listasocio'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "cod_soc"},
            {"data": "per.numdoc_per"},
            {"data": "per.nom_per"},
            {"data": "per.eda_per"},
            {"data": "per.sex_per.name"},
            {"data": "per.dir_per"},
            {"data": "per.numcel_per"},
            {"data": "per.ema_per"},
            {"data": "per.ema_per"},
        ],
        columnDefs: [
            // Opciones
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a href="/socio/editarsocio/' + row.per.id +'/" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                }
            },
            // Nombre Completo
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                    return row.per.nom_per + ' ' +row.per.apepat_per + ' ' + row.per.apemat_per
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
    $('input[name="per.numdoc_per"]').bind('keypress', function(event) {
        var regex = new RegExp("^[0-9]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
          event.preventDefault();
          return false;
        }
    });
    
    getData();
   
});
  
