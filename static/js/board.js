/**
 * Created by zxiaobai on 17/1/5.
 */
var msgTemplate = function(msg) {
  var m = msg
  var t = `
    <div style="margin-top: 5px;">
        <label style="margin-right: 10px;">${ m.created_time }</label>
        <a href="/profile/${ m.username }"><img style="position:relative;top:14px;height:40px;width:40px" src="/static/avatar/${ m.avatar }" class="circle z-depth-1"></a>
        <span style="margin-right: 10px;">
        <a style="color:mediumvioletred" href="/profile/${ m.username }">${ m.username }</a>:</span>
        <span>${ m.content }</span>
        <span class="right" style="color:red;position:relative;top:24px">new</span>
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
                $('.msgs').prepend(msgTemplate(r.data))
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
