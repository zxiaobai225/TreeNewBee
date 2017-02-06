/**
 * Created by zxiaobai on 17/2/5.
 */

var loadTemplate = function () {
    return `
    <div class="img-loading">
        <p style="text-align: center;font-size: 12px">加载中...</p>
        <div class="progress">
        <div class="indeterminate">
    </div>
    `
}


var bindBtnLoadGif = function () {
    $('.all-content').on('click', ".gif-btn", function () {
    var gif = $(this).siblings('.gif-img');
    var gif_url = gif.data('gif');
    if (gif[0].src == gif_url){
        return false
    }else {
        $(loadTemplate()).prependTo($(this).closest('.wifi-img'))
        gif.attr('src',gif_url)
        $(this).addClass('hide')
        gif.load(function(){
            $(this).siblings('.img-loading').slideUp('1000')
        });
    }
    })
};

var bindImgLoadGif = function () {
    $('.all-content').on('click', ".gif-img", function () {
    var gif = $(this);
    var gif_url = gif.data('gif');
    if (gif.prop('src') == gif_url){
        return false
    }else {
        $(loadTemplate()).prependTo($(this).closest('.wifi-img'))
        gif.attr('src',gif_url)
        $(this).siblings('.gif-btn').addClass('hide')
        gif.load(function(){
            $(this).siblings('.img-loading').slideUp('1000')
        });
    }
    })
};

var qiquTemplate = function (d) {
    template1 = `
    <li class="content z-depth-3">
        <div class="in-content">
            <span><img class="circle" style="width: 50px;height: 50px" src="${ d.avatar }"></span>
            <b style="color:mediumvioletred;position: relative;top:-17px;">${ d.username }</b>
            <p>${ d.title }</p>
            <p>${ d.content }</p>
        </div>
    `
    if(d.data_gif == ''){
        template2 = `
        <div class="wifi-img">
            <img style="width: 480px;" src=${ d.wifi_img_url }>
        </div>
        `
    }else{
        template2 = `
        <div class="wifi-img">
            <img class="gif-img" style="width: 480px;" src="${ d.wifi_img_url }" data-gif=${ d.data_gif }>
            <button id="gif-btn" class="btn gif-btn">点击图片加载GIF</button>
        </div>
    `
    }
    if(d.hot_comment != ''){
        template3 = `
            <div class="in-content">
                <p><span style="color: #de5025;">神评论：</span>${ d.hot_comment }</p>
            </div>
            <div class="like_dislike in-content">
                <span>顶:${ d.like }</span>
                <span>踩:${ d.dislike }</span>
            </div>
        </li>
    `
    }else{
        template3 = `
            <div class="like_dislike in-content">
                <span>顶:${ d.like }</span>
                <span>踩:${ d.dislike }</span>
            </div>
        </li>
    `
    }
    return template1+template2+template3
}


var bindEventAdd = function () {
        var data = {
            page: $('.all-content').data('page') + 1
        };
        var response = function (r) {
            if (r.success) {
                $('.all-content').data('page',data.page);
                for (var i=0; i<r.data.length; i++) {
                    var new_qiqu = $(qiquTemplate(r.data[i]));
                    var qiqu_cell = $('.cell');
                    new_qiqu.appendTo(qiqu_cell).slideDown()
                }
            } else {
                alertify.error(r.message)
            }
        };
        api.addQiqu(data.page, response)
    };


var scrollAddQiqu =function(){
    $(window).scroll(function(){
    　　var scrollTop = $(document).scrollTop();
    　　var scrollHeight = $(document).height();
    　　var windowHeight = $(this).height();
        // console.log("滚动条到顶部的垂直高度: "+scrollTop);
        // console.log("页面的文档高度 ："+scrollHeight);
        // console.log('浏览器的高度：'+windowHeight);
    　　if(eval(windowHeight+scrollTop) >= eval(scrollHeight - 50)){
        $('.loading').css('display','block');
        bindEventAdd();
    　　}
    });
};

$(document).ready(function () {
    bindBtnLoadGif();
    bindImgLoadGif();
    scrollAddQiqu();
});
