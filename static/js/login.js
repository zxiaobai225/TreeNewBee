/**
 * Created by zxiaobai on 16/12/28.
 */

$(document).ready(function() {
        $('.go-register').click(function () {
            $('.login-row').addClass('hide');
            $('.register-row').removeClass('hide');
            $('.register').removeClass('animated shake')
        });

        $('.go-login').click(function () {
            $('.register-row').addClass('hide');
            $('.login-row').addClass('animated flipInY').removeClass('hide');
            $('.login').removeClass('animated shake')
        });

        $("input").focus(function () {
            $(this).siblings('label').addClass('active');
            $(this).siblings('p').text('')
        });

        $("input").blur(function () {
            if($(this).val().length==0){
                $(this).siblings('label').removeClass('active');
            }
            var valLength = $(this).val().length;
            if(valLength>0 & valLength<6){
                $(this).siblings('p').text('用户名或密码至少为6位')
            }else {
                $(this).siblings('p').text('')
            }
          });

        $('input').on('input propertychange', function () {
            var usernameLength = $('.username').val().length;
            var passwordLength = $('.password').val().length;
            if(usernameLength>=6 & passwordLength>=6){
                $('.login-btn').removeClass('disabled');
            }else {
                $('.login-btn').addClass('disabled');
            }
        });

        $('input').on('input propertychange',function () {
            var usernameLength = $('.username1').val().length;
            var passwordLength = $('.password1').val().length;
            if(usernameLength>=6 & passwordLength>=6){
                $('.register-btn').removeClass('disabled');
            }else {
                $('.register-btn').addClass('disabled');
            }
        });

    })
