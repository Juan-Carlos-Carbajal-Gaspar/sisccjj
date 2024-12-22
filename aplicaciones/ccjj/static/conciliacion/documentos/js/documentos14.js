// Funcion para establecer minimo dos digitos para la fecha y hora automaticamente
function minTwoDigits(n) {
    return (n < 10 ? '0' : '') + n;
}
// Dias de la Semana
const dias = [
    "Domingo", // 0
    "Lunes", // 1
    "Martes", // 3
    "Miercoles", // 3
    "Jueves", // 4
    "Viernes", // 5
    "Sabado", // 6
  ];
//  alert(dias[formatNumDia(fechaaudiencia)]);
// Meses del Year
// Dias de la Semana
const meses = [
    "Enero", // 0
    "Febrero", // 1
    "Marzo", // 3
    "Abril", // 3
    "Mayo", // 4
    "Junio", // 5
    "Julio", // 6
    "Agosto", // 7
    "Septiembre", // 8
    "Octubre", // 9
    "Noviembre", // 10
    "Diciembre", // 11
  ];

// Formato General de Fecha Audiencia Para Documento
const formatDateAudienciaDoc = (fechaaudiencia)=>{
    var datofecha='el día ' + dias[fechaaudiencia.getDay()] 
    + ' ' + minTwoDigits(fechaaudiencia.getDate()) + ', de '
    + meses[(fechaaudiencia.getMonth() + 1)]
    + ', a horas ' + fechaaudiencia.getHours()
    + ':' + fechaaudiencia.getMinutes();
    return datofecha;
}



var tblDocumentos;
var tblOtrosDocumentos;

function getData(){
    tblDocumentos=$('#tblDocumentoConciliacion').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ordering: false,
        bAutoWidth:true,
        sScrollX:true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'listadocumentos'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "tip_doc"},
            {"data": "tip_doc"},
            {"data": "tip_doc"},
        ],
        columnDefs: [
            
            {
                targets: [-1], // Opcion Subir
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    if (row.arcesc_doc === null){
                        return ' <a href="#" rel="subirdoc" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Subir</a>';
                    }
                    else{
                        
                        return '<a href="'+ row.arcesc_doc +'" target="_blank" class="btn btn-success btn-xs btn-flat btnEdit"> <i class="fas fa-file-pdf"></i> Ver</a>' + '<a href="#" rel="subirdoc" class="btn btn-warning btn-xs btn-flat btnEdit"> <i class="fas fa-edit"></i> Editar</a>';
                    }                    
                }
            },
            {
                targets: [-2], // Opcion Descargar en word
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    if (row.t_doc == 'solicitud'){
                        
                        return '<a href="/gensolicitud/'+ row.id_exp +'/" target="_blank"> <i class="far fa-file-word"></i> Descargar</a>';
                    }
                    else if(row.t_doc == 'esquela'){
                        
                        return '<a href="/genesquelaconciliador/'+ row.id_exp +'/" target="_blank"> <i class="far fa-file-word"></i> Descargar</a>';
                    }
                    else if(row.t_doc == 'informeacta'){
                        
                        return '<a href="/generaracta/'+ row.id_exp +'/" target="_blank"> <i class="far fa-file-word"></i> Descargar</a>';
                    }
                    else{
                        return '...';
                    }                     
                }
            },
                        
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
    
    tblOtrosDocumentos=$('#tblOtrosDocumentoConciliacion').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ordering: false,
        bAutoWidth:true,
        sScrollX:true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'listaotrosdocumentos'
            },
            dataSrc: ""
        },
        columns: [
            // {"data": "idper"},
            {"data": "id"},
            {"data": "nombper"},
            {"data": "id_inv"},
        ],
        columnDefs: [
            
            {
                targets: [-1], // Opcion Subir
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    if (row.esc_invi === null){
                        return ' <a href="#" rel="subirotrosdoc" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Subir</a>';
                    }
                    else{
                        
                        return '<a href="'+ row.esc_invi +'" target="_blank" class="btn btn-success btn-xs btn-flat btnEdit"> <i class="fas fa-file-pdf"></i> Ver</a>' + '<a href="#" rel="subirotrosdoc" class="btn btn-warning btn-xs btn-flat btnEdit"> <i class="fas fa-edit"></i> Editar</a>';
                    }                    
                }
            },
            {
                targets: [-2], // Opcion Descargar en word
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var fechahora = row.fec_invi + 'T' + row.hor_invi;
                    var fechaaudiencia = new Date(fechahora);
                    
                    if (row.tip_invi == 'p'){
                        return '<a href="/genpriinvitacion/' + row.idexp +'/' + row.idper + '/' + formatDateAudienciaDoc(fechaaudiencia) + '/" target="_blank"> <i class="far fa-file-word"></i> Descargar</a>';
                    }
                    else if(row.tip_invi == 's'){
                        return '<a href="/genseginvitacion/' + row.idexp + '/' + row.idper + '/' + formatDateAudienciaDoc(fechaaudiencia) + '/" target="_blank"> <i class="far fa-file-word"></i> Descargar</a>';
                    }
                    else{
                        return '...';
                    }                     
                }
            },
            
            {
                targets: [-3], // Tipo Invitacion
                orderable: false,
                render: function (data, type, row) {
                    
                    if (row.tip_invi == 'p'){
                        return 'PRIMERA INVITACIÓN DE: ' + row.nombper;
                    }
                    else if(row.tip_invi == 's'){
                        return 'SEGUNDA INVITACIÓN DE: ' + row.nombper;
                    }
                    else{
                        return '...';
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

    // Validar campo de Archivo PDF
    
    // Para la etiqueta html
    modal_title=$('.modal-title');

    // -------------------------------//
    //---TABLA DOCUMENTOS-------------//
    //--------------------------------//
    // Para editar
    $('#tblDocumentoConciliacion tbody')
        // Ver Detalle Expediente
        .on('click', 'a[rel="subirdoc"]', function () {
            modal_title.find('span').html('Subir Documento');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblDocumentos.cell($(this).closest('td, li')).index();
            var data = tblDocumentos.row(tr.row).data();

            $('input[name="id"]').val(data.id);
            $('input[name="tipodocumento"]').val(data.tip_doc);
            $('#modalDocumentos').modal('show');
        })
    // -------------------------------//
    //---TABLA DOCUMENTOS-------------//
    //--------------------------------//

    // -------------------------------//
    //---TABLA OTROS DOCUMENTOS-------------//
    //--------------------------------//
    // Para editar
    $('#tblOtrosDocumentoConciliacion tbody')
        // Ver Detalle Expediente
        .on('click', 'a[rel="subirotrosdoc"]', function () {
            modal_title.find('span').html('Subir Otros Documentos');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblOtrosDocumentos.cell($(this).closest('td, li')).index();
            var data = tblOtrosDocumentos.row(tr.row).data();

            var tipodoc = '';

            if (data.tip_invi == 'p'){
                tipodoc = 'PRIMERA INVITACIÓN DE: ' + data.nombper;
            }
            else if(data.tip_invi == 's'){
                tipodoc = 'SEGUNDA INVITACIÓN DE: ' + data.nombper;
            }
            else{
                tipodoc = '...';
            }

            $('input[name="idotros"]').val(data.id);
            $('input[name="tipootrosdocumentos"]').val(tipodoc);
            $('#modalOtrosDocumentos').modal('show');
            
        })
    // -------------------------------//
    //---TABLA OTROS DOCUMENTOS-------------//
    //--------------------------------//


   
    // Para Subir el Documento de Conciliacion
    $('#formDocumentos').on('submit', function (e) {
        e.preventDefault();

        var archivopdf = $('input[name="archivo"]').val()
        var extension = /(.pdf)$/i;
        
        // var extension = /(.pdf|.jpeg|.png|.gif)$/i;
        if(!extension.exec(archivopdf)){
            message_error('Debe Subir Documento Con Extension PDF Unicamente');
            return false;
        }else{
            var parameters = $(this).serializeArray();
            var parameters = new FormData(this);
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('id', $('input[name="id"]').val());
            parameters.append('archivopdf', $('input[name="archivo"]').val());

            submit_with_ajax(
                window.location.pathname, 
                'Notificación', 
                '¿Estas seguro de Subir el archivo seleccionado?', 
                parameters, 
                function () {
                    $('#modalDocumentos').modal('hide');
                    getData();
                });
        }

    });

    // Para Subir Otros Documentos de Conciliacion
    $('#formOtrosDocumentos').on('submit', function (e) {
        e.preventDefault();

        var archivopdf = $('input[name="otroarchivo"]').val()
        var extension = /(.pdf)$/i;
        
        // var extension = /(.pdf|.jpeg|.png|.gif)$/i;
        if(!extension.exec(archivopdf)){
            message_error('Debe Subir Documento Con Extension PDF Unicamente');
            return false;
        }else{
            var parameters = $(this).serializeArray();
            var parameters = new FormData(this);
            parameters.append('action', 'subirotrosdocumento');
            parameters.append('id', $('input[name="idotros"]').val());
            parameters.append('archivopdf', archivopdf);

            submit_with_ajax(
                window.location.pathname, 
                'Notificación', 
                '¿Estas seguro de Subir el archivo seleccionado?', 
                parameters, 
                function () {
                    $('#modalOtrosDocumentos').modal('hide');
                    getData();
                });
        }

    });


});
  
