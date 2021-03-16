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

    // Attach info to the form
    form.submit(function(e){
        e.preventDefault();
        loadData(fd)
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

function loadData(fd) {
    // Load files
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
