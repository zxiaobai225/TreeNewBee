/**
 * Created by zxiaobai on 17/1/5.
 */
var msgTemplate = function(msg) {
  var m = msg
  var t = `
    <div style="margin-top: 5px;">
        <label style="margin-right: 10px;">${ m.created_time }</label>
        <span style="color:mediumvioletred">${ m.username }</span>
        <span>: ${ m.content }</span>
    </div>
  `
  return t
}

var bindEventAdd = function () {
    $('#add').click(function () {
        var parent = $('.board')
        var data = {
            content: parent.find('.content').val(),
        };
        var response = function (r) {
            if (r.success) {
                $('.msgs').append(msgTemplate(r.data))
                parent.find('.content').val('')
                alertify.success(r.message)
            } else {
                alertify.error(r.message)
            }
        };
        api.addBoardMsg(data, response)
    })
};

var bindEvents = function () {
    bindEventAdd();
};

$(document).ready(function () {
    bindEvents()
});
