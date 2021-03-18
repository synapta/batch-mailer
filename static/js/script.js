$(document).ready(function() {
    fd = new FormData();
    files = {}
    files['docx'] = {}
    files['xlsx'] = {}
    
    var docx_container = $('#docx_upload');
    var xlsx_container = $('#xlsx_upload');
    
    // Set drag and drop listeners
    setDragListeners(docx_container, fd)
    setDragListeners(xlsx_container, fd)

    // Set upload listeners to input types
    $('#docx_input').on('change', function () {
        handleDocXUpload(this.files, fd);
    });
    $('#xlsx_input').on('change', function () {
        handleXlsXUpload(this.files, fd);
    });

    // Prevent submit behaviour and validate the included data
    var validation_form = $('form#validation')
    validation_form.submit(function(e){
        e.preventDefault();
        e.stopPropagation()
        validateData(fd)
    });
});


function setDragListeners(container, fd) {
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

    if (!$.isEmptyObject(files['docx'])) {
        exist_docx = true
        if (files['docx'].type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
            is_docx = true
        }
    }

    if (!$.isEmptyObject(files['xlsx'])) {
        exist_xlsx = true
        if (files['xlsx'].type == 'text/csv') { //TODO: aggiungi la gestione dell'xslx
            is_xlsx = true
        }
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
            xlsx_error.append('Attenzione: sembra che il file caricato non sia nel formato .xlsx o .csv!')
            xlsx_input.addClass('is-invalid')
        }
    }

    if (exist_docx && exist_xlsx && is_docx && is_xlsx)
        local_check = true

    return local_check
}


function serverSideCheck(fd) {
    $.ajax({
        url: '/',
        type: 'POST',
        data: fd,
        processData: false,
        contentType: false,
        success: function(res) {
            // Process server response
            processServerCheck(res)           
        }
    });
}


function processServerCheck(res) {
    var docx_input = $('input#docx_input')
    var docx_error = $('div#docx_feedback')
    var xlsx_input = $('input#xlsx_input')
    var xlsx_error = $('div#xlsx_feedback')
    if (res['field'] == 'OK') {
        preview_data = {'subject': res['data']['subject'],
                        'recipient': res['data']['recipient'],
                        'body': res['data']['body'],
                        'lines': res['data']['lines']}
        $.ajax({
            type: 'POST',
            url: '/preview',
            data: JSON.stringify(preview_data),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: function (data) {
                $('body').empty();
                $('body').hide(); 
                $('body').append(data);
                $('body').show();                
            }
        });
    }

    if (res['field'] == 'xlsx') {
        xlsx_error.append(res['text'])
        xlsx_input.addClass('is-invalid')
        return
    }

    if (res['field'] == 'both') {
        docx_error.append(res['text_docx'])
        docx_input.addClass('is-invalid')
        xlsx_error.append(res['text_xlsx'])
        xlsx_input.addClass('is-invalid')
        return
    }
}