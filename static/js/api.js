/**
 * Created by zxiaobai on 17/1/5.
 */

var api = {}

api.ajax = function (url, method, form, callback) {
    var request = {
        url: url,
        type: method,
        data: form,
        success: function (response) {
            var r = JSON.parse(response)
            callback(r)
        },
        error: function (response) {
            var r = {
                'success': false,
                message: '网络错误'
            }
            callback(r)
        }
    }
    $.ajax(request)
}

api.get = function (url, response) {
    api.ajax(url, 'get', {}, response)
}

api.post = function (url, form, response) {
    api.ajax(url, 'post', form, response)
}

api.userLogin = function (form, response) {
    var url = '/login'
    api.post(url, form, response)
}

api.userRegister = function (form, response) {
    var url = '/register'
    api.post(url, form, response)
}

// api.userGetcode = function (form, response) {
//     var url = '/mail/send'
//     api.post(url, form, response)
// }

api.profileUpdate = function (form, response) {
    var url = '/profile/update'
    api.post(url, form, response)
}

api.addBoardMsg = function (form, response) {
    var url = '/board/add'
    api.post(url, form, response)
}

api.addWeibo = function (form, response) {
    var url = '/weibo/add'
    api.post(url, form, response)
}

api.addWeiboComment = function (form, response) {
    var url = '/weibo/comment/add'
    api.post(url, form, response)
}

api.likeWeibo = function (weibo_id, response) {
    var url = '/weibo/like/'+ weibo_id
    api.get(url, response)
}

api.addQiqu = function (page, response) {
    var url = '/qiqu?page='+ page
    api.get(url, response)
}
