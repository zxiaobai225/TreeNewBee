/**
 * Created by zxiaobai on 17/1/5.
 */

var successView = function (p) {
    p.parent().addClass('animated fadeOutUpBig')
}

var bindEventLogin = function () {
    $('.login-btn').click(function () {
        if ($(this).hasClass('disabled')) {
            return false
        }
        var parent = $(this).parents('.login')

        var data = {
            username: parent.find(':input.username').val(),
            password: parent.find(':input.password').val(),

        };

        $('.login').removeClass('animated shake')
        var response = function (r) {
            if (r.success) {
                successView(parent.parents('.container'))
                location.href = "/"
            } else {
                alertify.error(r.message)
                $('.login').addClass('animated shake')
            }
        };
        api.userLogin(data, response)
    })
};

var bindEventRegister = function () {
    $('.register-btn').click(function () {
        if ($(this).hasClass('disabled')) {
            return false
        }
        var parent = $(this).parents('.register')

        var data = {
            username: parent.find(':input.username1').val(),
            password: parent.find(':input.password1').val(),
            email: parent.find(':input.email').val(),
            code: parent.find(':input.code').val(),
        };

        $('.register').removeClass('animated shake')
        var response = function (r) {
            if (r.success) {
                successView(parent.parents('.container'))
                location.href = "/"
            } else {
                alertify.error(r.message)
                $('.register').addClass('animated shake')
            }
        };
        api.userRegister(data, response)
    })
};

var bindEventGetcode = function () {
    $('.get-code').click(function () {

        var parent = $(this).parents('.register')

        var data = {
            email: parent.find(':input.email').val(),
        };

        $('.register').removeClass('animated shake')
        var response = function (r) {
            if (r.success) {
                $(".get-code").attr("disabled", true);
                var count = 30;
                var countdown = setInterval(CountDown, 1000);
                function CountDown() {
                    $(".get-code").attr("disabled", true);
                    $(".get-code").text("稍等"+count+"s");
                    if (count == 0) {
                        $(".get-code").text("重新获取").removeAttr("disabled");
                        clearInterval(countdown);
                    }
                    count--;
                }
                alertify.success(r.message)
            } else {
                alertify.error(r.message)
                $('.register').addClass('animated shake')
            }
        };
        api.userGetcode(data, response)
    })
};

var bindEvents = function () {
    bindEventLogin();
    bindEventRegister();
    bindEventGetcode();
};

$(document).ready(function () {
    bindEvents()
});
