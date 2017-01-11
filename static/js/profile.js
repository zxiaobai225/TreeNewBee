/**
 * Created by zxiaobai on 17/1/5.
 */

var bindEventUpdate = function () {
    $('#update').click(function () {
        var parent = $('.profile')
        var data = {
            password: parent.find(':input.password').val(),
            qq: parent.find(':input.qq').val(),
            signature: parent.find('.signature').val(),
        };
        var response = function (r) {
            if (r.success) {
                alertify.success(r.message)
            } else {
                alertify.error('未知错误')
            }
        };
        api.profileUpdate(data, response)
    })
};

var bindEvents = function () {
    bindEventUpdate();
};

$(document).ready(function () {
    bindEvents()
});
