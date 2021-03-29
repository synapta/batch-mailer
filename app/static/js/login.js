$(document).ready(function() {
    // Prevent submit behaviour and validate the login information
    var login_form = $('form#login')
    login_form.submit(function(e){
        e.preventDefault();
        e.stopPropagation();
        validateLogin();
    });

    // Loading overlay
    $.LoadingOverlaySetup({
        background       : 'rgba(0, 0, 0, 0.8)',
        image            : '',
        imageAnimation   : 'rotate_right',
        imageColor       : '#ffcc00',
        text             : 'Connessione al server di posta',
        textColor        : '#FFFFFF',
        textAutoResize   : true,
        textResizeFactor : 0.5,
        fontawesome      : 'fa fa-cog fa-spin'      
    });
});

function validateLogin() {
    valid = true;

    // Check address
    var email = $('#mailAddress');
    var email_invalid = $('#email_feedback');
    var mail_reg = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    
    email.removeClass('is-invalid');
    email_invalid.empty();
    
    if (email.val().trim() == '') {
        email.addClass('is-invalid');
        email_invalid.append('Attenzione: non hai inserito alcun indirizzo email');
        valid = false;
    } else if(!mail_reg.test(email.val().trim())) {
        email.addClass('is-invalid');
        email_invalid.append('Attenzione: l\'indirizzo email inserito non sembra valido');
        valid = false;
    }

    // Check password
    var pwd = $('#mailPassword');
    var pwd_invalid = $('#password_feedback');

    pwd.removeClass('is-invalid');
    pwd_invalid.empty();
    
    if (pwd.val().trim() == '') {
        pwd.addClass('is-invalid');
        pwd_invalid.append('Attenzione: non hai inserito alcuna password');
        valid = false;
    }
    
    // Check server
    var server = $('#mailServer');
    var server_invalid = $('#server_feedback');
    var server_reg = /^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$/;

    server.removeClass('is-invalid');
    server_invalid.empty();

    if (server.val().trim() == '') {
        server.addClass('is-invalid');
        server_invalid.append('Attenzione: non hai inserito alcun indirizzo del server');
        valid = false;
    } else if(!server_reg.test(server.val().trim())) {
        server.addClass('is-invalid');
        server_invalid.append('Attenzione: l\'indirizzo del server inserito non sembra valido');
        valid = false;
    }
    
    // Check port
    var port = $('#mailPort');
    var port_invalid = $('#port_feedback');

    port.removeClass('is-invalid');
    port_invalid.empty();

    if (port.val().trim() == '') {
        port.addClass('is-invalid');
        port_invalid.append('Attenzione: non hai inserito alcun indirizzo del server');
        valid = false;
    } else if (!Number.isInteger(Number.parseInt(port.val().trim()))) {
        port.addClass('is-invalid');
        port_invalid.append('Attenzione: il valore di porta inserito non è un numero');
        valid = false;
    }

    if (valid) {
        validateLoginServer()
    }
}

function validateLoginServer(){
    var form_data = $('.form').serialize();
    var general = $('#general');
    var general_invalid = $('#general_feedback');
    general.removeClass('is-invalid');
    general_invalid.empty();
    
    $.ajax({
        type:'POST',
        url:'/login',
        data: form_data,
        encode: true,
        beforeSend: function() {
            $.LoadingOverlay('show');
        }
    }).done(function(data){
        $.LoadingOverlay('hide');
        console.log(data)
        if (data == 'OK') {
            $('.index-button').click()
        } else {
            console.log('general')
            console.log(general)
            general.addClass('is-invalid');
            general_invalid.append(data)
        }
    }).fail(function(data){
        $.LoadingOverlay('hide');
        general.addClass('is-invalid');
        general_invalid.append('Attenzione: impossibile collegarsi al server locale')
    });
}