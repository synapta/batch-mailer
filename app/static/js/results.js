$(document).ready(function() {
    var form = $('form#control')
    form.submit(function(e){
        e.preventDefault();
        e.stopPropagation()
    });

    // Trigger send-button click
    $('#back-index-button').click(function() {
        $('.back-button').click();
    });
});