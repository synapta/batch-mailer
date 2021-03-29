$(document).ready(function () {
    fd = new FormData();
    files = {}
    files['docx'] = {}
    files['xlsx'] = {}

    var docx_upload = $('#docx_upload');
    var xlsx_upload = $('#xlsx_upload');

    // Set drag and drop listeners
    setDragListeners(docx_upload, fd)
    setDragListeners(xlsx_upload, fd)

    // Set upload listeners to input types
    $('#docx_input').on('change', function () {
        handleDocXUpload(this.files, fd);
    });
    $('#xlsx_input').on('change', function () {
        handleXlsXUpload(this.files, fd);
    });

    // Prevent submit behaviour and validate the included data
    var validation_form = $('form#validation')
    validation_form.submit(function (e) {
        e.preventDefault();
        e.stopPropagation()
        validateData(fd)
    });

    // Loading overlay
    $.LoadingOverlaySetup({
        background: 'rgba(0, 0, 0, 0.8)',
        image: '',
        imageAnimation: 'rotate_right',
        imageColor: '#ffcc00',
        text: 'Sto processando i file e verificando gli allegati',
        textColor: '#FFFFFF',
        textAutoResize: true,
        textResizeFactor: 0.5,
        fontawesome: 'fa fa-cog fa-spin'
    });
});

// Reset functions
function reset_docx() {
    var input = $('#docx_input');
    var upload = $('#docx_upload');
    var valid = $('#docx-valid-feedback');
    var invalid = $('#docx-invalid-feedback');
    input.removeClass('is-invalid');
    input.removeClass('is-valid');
    upload.removeClass('valid-border');
    upload.removeClass('invalid-border');
    valid.empty();
    invalid.empty();
}

function reset_xlsx() {
    var input = $('#xlsx_input');
    var upload = $('#xlsx_upload');
    var valid = $('#xlsx-valid-feedback');
    var invalid = $('#xlsx-invalid-feedback');
    input.removeClass('is-invalid');
    input.removeClass('is-valid');
    upload.removeClass('valid-border');
    upload.removeClass('invalid-border');
    valid.empty();
    invalid.empty();
}


function setDragListeners(container, fd) {
    container.on({
        'dragenter': function (e) {
            e.preventDefault();
        },
        'dragleave': function (e) {
        },
        'drop': function (e) {
            e.preventDefault()
            if (e.target.id == 'docx_input') {
                handleDocXUpload(e.originalEvent.dataTransfer.files, fd);
            } else if (e.target.id == 'xlsx_input') {
                handleXlsXUpload(e.originalEvent.dataTransfer.files, fd)
            }
        },
        'dragover': function (e) {
            e.preventDefault();
        }
    });
}


function handleDocXUpload(f, fd) {
    f = f[0]
    files['docx'] = f
    fd.delete('docx_file')
    fd.append('docx_file', files['docx']);
    
    reset_docx();
    var input = $('#docx_input');
    var upload = $('#docx_upload');
    var valid = $('#docx-valid-feedback');
    input.addClass('is-valid');
    upload.addClass('valid-border');
    valid.append('File caricato: ' + f['name']);
    $('#docx_upload h6').empty();
}


function handleXlsXUpload(f, fd) {
    f = f[0]
    files['xlsx'] = f
    fd.delete('xlsx_file')
    fd.append('xlsx_file', files['xlsx']);

    reset_xlsx();
    var input = $('#xlsx_input');
    var upload = $('#xlsx_upload');
    var valid = $('#xlsx-valid-feedback');
    input.addClass('is-valid');
    upload.addClass('valid-border');
    valid.append('File caricato: ' + f['name']);
    $('#xlsx_upload h6').empty();
}


function validateData(fd) {
    // Load files
    for (var value of fd.values()) {
        console.log('Loaded file:');
        console.log(value)
    }

    if (localSideCheck(fd))
        serverSideCheck(fd)
}


function localSideCheck(fd) {
    local_check = false
    
    reset_docx();
    reset_xlsx();
    
    var docx_input = $('#docx_input');
    var docx_upload = $('#docx_upload');
    var docx_invalid = $('#docx-invalid-feedback');
    var xlsx_input = $('#xlsx_input');
    var xlsx_upload = $('#xlsx_upload');
    var xlsx_invalid = $('#xlsx-invalid-feedback');

    // check existence and file type correcteness
    exist_docx = false
    exist_xlsx = false
    is_docx = false
    is_xlsx = false

    var re = /(?:\.([^.]+))?$/;

    if (!$.isEmptyObject(files['docx'])) {
        exist_docx = true;
        if (files['docx'].type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
            re.exec(files['docx'].name)[1] == 'docx') {
            is_docx = true;
        }
    }

    if (!$.isEmptyObject(files['xlsx'])) {
        exist_xlsx = true;
        if (files['xlsx'].type == 'text/csv' || re.exec(files['xlsx'].name)[1] == 'csv') {
            is_xlsx = true;
        } else if (files['xlsx'].type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
            re.exec(files['xlsx'].name)[1] == 'xlsx') {
            is_xlsx = true;
        }
    }

    if (!exist_docx) {
        docx_invalid.append('Attenzione: sembra che tu non abbia caricato alcun documento!');
        docx_input.addClass('is-invalid');
        docx_upload.addClass('invalid-border');
    } else {
        if (!is_docx) {
            docx_invalid.append('Attenzione: sembra che il file caricato non sia nel formato .docx!');
            docx_input.addClass('is-invalid');
            docx_upload.addClass('invalid-border');
        }
    }

    if (!exist_xlsx) {
        xlsx_invalid.append('Attenzione: sembra che tu non abbia caricato alcun file per le variabili!');
        xlsx_input.addClass('is-invalid');
        xlsx_upload.addClass('invalid-border');
    } else {
        if (!is_xlsx) {
            xlsx_invalid.append('Attenzione: sembra che il file caricato non sia nel formato .xlsx o .csv!');
            xlsx_input.addClass('is-invalid');
            xlsx_upload.addClass('invalid-border');
        }
    }

    if (exist_docx && exist_xlsx && is_docx && is_xlsx)
        local_check = true;

    return local_check
}


function serverSideCheck(fd) {
    $.ajax({
        url: '/index',
        type: 'POST',
        data: fd,
        processData: false,
        contentType: false,
        beforeSend: function () {
            $.LoadingOverlay('show');
        },
        success: function (res) {
            $.LoadingOverlay('hide');
            processServerResponse(res);
        }
    });
}


function processServerResponse(res) {
    var docx_input = $('#docx_input');
    var docx_upload = $('#docx_upload');
    var docx_invalid = $('#docx-invalid-feedback');
    var xlsx_input = $('#xlsx_input');
    var xlsx_upload = $('#xlsx_upload');
    var xlsx_invalid = $('#xlsx-invalid-feedback');

    if (res == 'OK') {
        $('.preview-button').click();
    }

    if (res['field'] == 'xlsx') {
        xlsx_invalid.append(res['text']);
        xlsx_input.addClass('is-invalid');
        xlsx_upload.addClass('invalid-border');

        return
    }

    if (res['field'] == 'both') {
        docx_invalid.append(res['text_docx']);
        docx_input.addClass('is-invalid');
        docx_upload.addClass('invalid-border');
        xlsx_invalid.append(res['text_xlsx']);
        xlsx_input.addClass('is-invalid');
        xlsx_upload.addClass('invalid-border');

        return
    }
}