$(document).ready(function() {
    
    // Prevent submit behaviour
    var check_form = $('form#check')
    check_form.submit(function(e){
        e.preventDefault();
        e.stopPropagation()
    });

    // Trigger send-button click
    $('#index-button').click(function() {
        $('.back-button').click()
    });
});