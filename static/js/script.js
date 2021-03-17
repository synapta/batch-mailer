$(document).ready(function() {
    fd = new FormData();
    files = {}
    files['docx'] = {}
    files['xlsx'] = {}
    
    var docx_container = $('#docx_upload');
    var xlsx_container = $('#xlsx_upload');
    var form = $('form')
    
    // Set drag and drop listeners
    setListeners(docx_container, fd)
    setListeners(xlsx_container, fd)

    // Set upload listeners to input types
    $('#docx_input').on('change', function () {
        handleDocXUpload(this.files, fd);
    });
    $('#xlsx_input').on('change', function () {
        handleXlsXUpload(this.files, fd);
    });

    // Prevent submit behaviour and check the data
    form.submit(function(e){
        e.preventDefault();
        e.stopPropagation()
        validateData(fd)
    });
});


function setListeners(container, fd) {
    container.on({
        'dragenter': function (e) {
            e.preventDefault();
            // msgHolder.html("Drop here");
        },
        'dragleave': function (e) {
            // msgHolder.html("Click / Drop file to select.");
        },
        'drop': function (e) {
            e.preventDefault()
            if (e.target.id == 'docx_upload') {
                handleDocXUpload(e.originalEvent.dataTransfer.files, fd);
            } else if (e.target.id == 'xlsx_upload') {
                handleXlsXUpload(e.originalEvent.dataTransfer.files, fd)
            }  
        },
        'dragover' : function (e) {
            e.preventDefault();
        }
    });
}


function handleDocXUpload(f, fd) {
    f = f[0]
    files['docx'] = f
    fd.delete('docx_file')
    fd.append('docx_file', files['docx']);
}


function handleXlsXUpload(f, fd) {
    f = f[0]
    files['xlsx'] = f
    fd.delete('xlsx_file')
    fd.append('xlsx_file', files['xlsx']);
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
    
    var form = $('form')

    var docx_input = $('input#docx_input')
    var docx_error = $('div#docx_feedback')
    docx_input.removeClass('is-invalid')
    docx_error.empty()

    var xlsx_input = $('input#xlsx_input')
    var xlsx_error = $('div#xlsx_feedback')
    xlsx_input.removeClass('is-invalid')
    xlsx_error.empty()

    // check existence and file type correcteness
    exist_docx = false
    exist_xlsx = false
    is_docx = false
    is_xlsx = false
    i = 0
    for (var value of fd.values()) {
        if (i == 0) {
            exist_docx = true
            if (value.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
                is_docx = true
            }
        }
        if (i==1) {
            exist_xlsx = true
            if (value.type == 'text/csv') { //TODO: aggiungi la gestione dell'xslx
                is_xlsx = true
            }
        }
        i++
    }

    if (!exist_docx) {
        docx_error.append('Attenzione: sembra che tu non abbia caricato alcun documento!')
        docx_input.addClass('is-invalid')
    } else {
        if (!is_docx) {
            docx_error.append('Attenzione: sembra che il file caricato non sia nel formato .docx!')
            docx_input.addClass('is-invalid')
        }
    }

    if (!exist_xlsx) {
        xlsx_error.append('Attenzione: sembra che tu non abbia caricato alcun file per le variabili!')
        xlsx_input.addClass('is-invalid')
    } else {
        if (!is_xlsx) {
            xlsx_error.append('Attenzione: sembra che il file caricato non sia nel formato .docx!')
            xlsx_input.addClass('is-invalid')
        }
    }

    if (exist_docx && exist_xlsx && is_docx && is_xlsx)
        local_check = true

    return local_check









    /*
    console.log(fd)
    console.log(fd.values()['docx'])
    console.log(fd.values()['xlsx'])
    docx_input.addClass('is-invalid')
    var docx_input = $('docx_input')
    docx_input.removeClass('is-valid')
    docx_input.addClass('is-invalid')
    form.addClass('was-validated')
    */
}


function serverSideCheck(fd) {
    $.ajax({
        url: '/',
        type: 'POST',
        data: fd,
        processData: false,
        contentType: false,
        success: function() {
            //TODO
        }
    });
}
