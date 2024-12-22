// Declaramos variable tblperiodo para la tabla de datos
var tblperiodo;
function getData(){
    tblperiodo=$('#data').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'readperiodo'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "per_pe"},
            {"data": "num_exp"},
            {"data": "num_act"},
            {"data": "num_inf"},
            {"data": "est_pe"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/periodo/editarperiodo/' + row.id + '/" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if(row.est_pe == 'a'){
                        return 'Activo';
                    }else{
                        return 'Inactivo';
                    }
                }
            },
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
  }

$(function () {
         
    // Para Cargar los datos a la tabla
    getData();

});
  
  