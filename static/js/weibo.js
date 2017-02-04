/**
 * Created by zxiaobai on 17/2/3.
 */

var weiboTemplate = function (w) {
    return `
    <div class="z-depth-3 weibo-item" data-id="${ w.id }">
        <div class="weibo-item-1">
            <div class="weibo-avartar">
                <a href="/profile/${ w.username }">
                    <img class="z-depth-2 circle avatar" src="/static/avatar/${ w.avatar }">
                </a>
            </div>
            <div class="weibo-item-2" style="margin-left: 60px;">
                <div class="weibo-username"><a href="/profile/${ w.username }"><b>${ w.username }</b></a></div>
                <div class="weibo-created-time"><p>${ w.created_time }</p></div>
                <div class="weibo-content"><p>${ w.weibo }</p></div>
            </div>
        </div>
        <div class="weibo-item-3">
            <a class="show-comment" href="javascript:">评论 <span>0</span></a>
            <a class="zan" href="javascript:">赞 <span>0</span></a>
        </div>
    <div class="comment-items" style="display:none;">
        <div class="weibo-comments-add">
            <textarea class="materialize-textarea comment" name="comment" length="50"></textarea>
            <button class="add-comment waves-effect waves-purple btn">发表评论</button>
        </div>
        <div class="weibo-comments">
        </div>
    </div>
    </div>
`
}

var commentTemplate = function (c) {
    return `
            <div class="comment-avatar">
                <a href="/profile/${ c.username }">
                    <img class="z-depth-2" src="/static/avatar/${ c.avatar }">
                </a>
            </div>
            <div class="weibo-comment">
                <div class="comment-username"><a href="/profile/${ c.username }">${ c.username }</a>: <span>${ c.comment }</span></div>
                <div class="comment-created-time"><p>${ c.created_time }</p></div>
            </div>
`
}

var bindShowComment = function () {
    $('.weibo').on('click', ".show-comment", function () {
        var comments = $(this).closest('.weibo-item').find('.comment-items');
        comments.slideToggle(500)
    })
};

var bindWeiboLike = function () {
    $('.weibo').on('click', ".zan", function () {
        var weibo_id = $(this).closest('.weibo-item').data('id');
        var like_nums = $(this).find('span');
        var response = function (r) {
            if (r.success) {
                like_nums.text(r.data['like_nums']);
                alertify.success(r.message)
            } else {
                alertify.error('网络错误')
            }
        };
        api.likeWeibo(weibo_id, response)
    })
};

var bindEventAdd = function () {
    $('#add').click(function () {
        if($(this).hasClass('disabled')){
            alertify.error('您发的太快啦')
            return false
        }
        var parent = $('.weibo');
        var data = {
            weibo: parent.find('.content').val(),
        };
        var response = function (r) {
            if (r.success) {
                $('#add').addClass("disabled");
                parent.find('.content').val('')
                var count = 30;
                var countdown = setInterval(CountDown, 1000);
                function CountDown() {
                    $('#add').addClass("disabled");
                    $('#add').text("稍等"+count+"s");
                    if (count == 0) {
                        $('#add').text("发微博").removeClass("disabled");
                        clearInterval(countdown);
                    }
                    count--;
                }
                var new_weibo = $(weiboTemplate(r.data))
                var weibo_cell = $('.weibo-items')
                new_weibo.prependTo(weibo_cell)
                alertify.success(r.message)
            } else {
                alertify.error(r.message)
            }
        };
        api.addWeibo(data, response)
    })
};

var bindEventAddComment = function () {
        $('.weibo').on('click', ".add-comment", function () {
        if($(this).hasClass('disabled')){
            alertify.error('您发的太快啦');
            return false
        }
        var comment = $(this).parent().find('.comment');
        var weibo = $(this).closest('.weibo-item');
        var data = {
            comment: comment.val(),
            weibo_id: weibo.data('id')
        };

        var response = function (r) {
            if (r.success) {
                weibo.find('.add-comment').addClass("disabled");
                comment.val('')
                var count = 30;
                var countdown = setInterval(CountDown, 1000);
                function CountDown() {
                    weibo.find('.add-comment').addClass("disabled");
                    weibo.find('.add-comment').text("稍等"+count+"s");
                    if (count == 0) {
                        weibo.find('.add-comment').text("发表评论").removeClass("disabled");
                        clearInterval(countdown);
                    }
                    count--;
                }
                var new_comment = $(commentTemplate(r.data))
                var comment_cell = weibo.find('.weibo-comments')
                new_comment.prependTo(comment_cell)
                alertify.success(r.message)
            } else {
                alertify.error(r.message)
            }
        };
        api.addWeiboComment(data, response)
    })
};


var bindEvents = function () {
    bindShowComment();
    bindWeiboLike();
    bindEventAdd();
    bindEventAddComment();
};

$(document).ready(function () {
    bindEvents()
});
