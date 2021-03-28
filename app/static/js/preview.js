$(document).ready(function() {

    // Loading overlay
    $.LoadingOverlaySetup({
        background       : 'rgba(0, 0, 0, 0.8)',
        image            : '',
        imageAnimation   : 'rotate_right',
        imageColor       : '#ffcc00',
        text             : 'Sto procedendo con l\'invio delle mail',
        textColor        : '#FFFFFF',
        textAutoResize   : true,
        textResizeFactor : 0.5,
        fontawesome      : 'fa fa-cog fa-spin'      
    });
    
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

    // Send form
    var send_form = $('form#send')
    send_form.submit(function(e){
        $.LoadingOverlay('show');
    });
});