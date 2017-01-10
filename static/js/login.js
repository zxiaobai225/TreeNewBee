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

            var valLength = $(this).val().length;
            if ($(this).hasClass('username1') & valLength>0 & valLength< 6) {
                $(this).siblings('p').text('用户名至少为6位')
            } else if ($(this).hasClass('password1') & valLength>0 & valLength< 6) {
                $(this).siblings('p').text('密码至少为6位')
            } else if ($(this).hasClass('code') & valLength>0 & valLength< 6) {
                $(this).siblings('p').text('验证码为6位')
            } else if ($(this).hasClass('email')
                & !$(".email").val().match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)
                & $(".email").val().length>0){
                $(this).siblings('p').text('邮箱格式不正确')
            }
             else {
                $(this).siblings('p').text('')
            }
            if ($(this).val().length == 0) {
                $(this).siblings('label').removeClass('active');
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
            var codeLength = $('.code').val().length;
            if(usernameLength>=6 & passwordLength>=6 & codeLength==6 ){
                $('.register-btn').removeClass('disabled');
            }else {
                $('.register-btn').addClass('disabled');
            }
            var email=$(".email").val();
            if(email.length==0){
                $('.register-btn').addClass('disabled');
            }
            if(!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)){
                $('.register-btn').addClass('disabled');
            }
        });

    })
