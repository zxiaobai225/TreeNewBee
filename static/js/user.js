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
            password: parent.find(':input.password').val()
        };

        $('.login').removeClass('animated shake')
        var response = function (r) {
            if (r.success) {
                successView(parent.parents('.father'))
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
            password: parent.find(':input.password1').val()
        };

        $('.register').removeClass('animated shake')
        var response = function (r) {
            if (r.success) {
                successView(parent.parents('.father'))
                location.href = "/"
            } else {
                alertify.error(r.message)
                $('.register').addClass('animated shake')
            }
        };
        api.userRegister(data, response)
    })
};


var bindEvents = function () {
    bindEventLogin();
    bindEventRegister()
};

$(document).ready(function () {
    bindEvents()
});
