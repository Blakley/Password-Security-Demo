// client-side script
$(document).ready(function() {

    // generates a captcha
    function generate() {
        let route = '/secureweb/captcha_generate/';

        $.get(route, function(data) {
            let captcha = data.captcha;
            // Set the captcha image source and hash value
            $("#captcha-img").attr("src", captcha);

        }, 'json');

        // show captcha, disable login form
        $(".captcha-area").show(); 
    }

    // attempts login
    function login(login_form) {
        // construct login post route
        let route = '/secureweb/login/'
        let form_id = '#login-form-' + login_form;

        // submit login, check status
        $.post(route, $(form_id).serialize(), function(data) {
            // login logic
            if (data.message) {
                // change color of if correct/incorrect login
                let statusColor = '#dc3545';
                if (data.message == 'correct') {
                    statusColor = '#28a745';
                }
    
                // update status element
                $('#status' + login_form).text(data.message).css('color', statusColor);
            }

            // reset input forms
            $(form_id)[0].reset();
        }, 'json');
    }

    /* User login submission */
    $('.user-login-form').submit(function(event) {
        event.preventDefault();

        // get login form number
        let login_form = $(this).attr('id').replace('login-form-', '');

        // trigger captcha for login #3
        if (login_form == 3) {
            // disable login form
            $("#login-form-3").addClass("blur-effect");
            $("#login-form-3 :input").prop("disabled", true);

            generate();
            return;
        }

        // submit login
        login(login_form);

        // reset login form
        this.reset();
    });

    /* User captcha submission */
    $("#captcha_input").on("keyup", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();

            // get user answer
            let answer = $(this).val();
    
            // extract captcha name
            let img = $("#captcha-img").attr("src");
            let captcha_name = img.substring(img.lastIndexOf('/') + 1);
    
            // get form submission data
            let form = {
                captcha_input: answer,
                captcha_name: captcha_name
            }
    
            let route = '/secureweb/captcha_submit/';
    
            // submit captcha, check status
            $.post(route, form, function(data) {
                // check captcha
                if (data.message == 'correct') {
                    // correct, submit login
                    $(".captcha-area").hide();
                    $("#login-form-3 :input").prop("disabled", false);
                    $("#login-form-3").removeClass("blur-effect");
                    $("#captcha-status").text('');

                    login(3);
                }
                else {
                    // incorrect, generate new captcha
                    $("#captcha-status").text(data.message);
                    $(this).val('');
                    generate();
                }
            }, 'json');
    
            // reset login form
            $(this).val('');
        }
    });

});
