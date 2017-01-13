/**
 * Created by zxiaobai on 17/1/12.
 */
    // 频道和消息
    var chatStore = {
        '大厅': [],
        '游戏': [],
        '灌水': [],
    };
    var currentChannel = '';

    var log = function(){
      console.log(arguments);
    };

    // 滚动到底部
    var scrollToBottom = function(selector){
        var height = $(selector).prop("scrollHeight");
        $(selector).animate({
            scrollTop: height
        }, 300);
    };

    var chatItemTemplate = function(chat) {
        var name = chat.name;
        var content = chat.content;
        var time = chat.created_time;
        var avatar = chat.avatar;
        var t = `
        <div class="chat-item burstStart read burstFinal">
            <div class="chat-item__container">
                <div class="chat-item__aside chat-avatar">
                    <div class="chat-item__avatar">
                        <span class="widget">
                            <div class="trpDisplayPicture avatar-s">
                                <img src="/static/avatar/${avatar}" class="circle z-depth-1" height="40" width="40" class="avatar__image" alt="">
                            </div>
                        </span>
                    </div>
                </div>
                <div class="chat-item__actions js-chat-item-actions">
                    <i class="chat-item__icon icon-check chat-item__icon--read chat-item__icon--read-by-some js-chat-item-readby"></i>
                    <i class="chat-item__icon icon-ellipsis"></i>
                </div>
                <div class="chat-item__content chat-content">
                    <div class="chat-item__details">
                        <div style="color:mediumvioletred" class="chat-item__from js-chat-item-from">${name}</div>
                        <span style="color:lightblue" class="chat-item__time js-chat-time" href="#">
                            <time data-time="${time}"></time>
                        </span>
                    </div>
                    <div class="chat-item__text js-chat-item-text" style="margin-top: 5px;">
                        <span class="my-content">${content}</span>
                    </div>
                </div>
            </div>
        </div>
        `;
        return t;
    };

    var insertChats = function(chats) {
        var selector = '#id-div-chats'
        var chatsDiv = $(selector);
        var html = chats.map(chatItemTemplate);
        chatsDiv.append(html.join(''));
        scrollToBottom(selector);
    };

    var insertChatItem = function(chat) {
        var selector = '#id-div-chats'
        var chatsDiv = $(selector);
        var t = chatItemTemplate(chat);
        chatsDiv.append(t);
        scrollToBottom(selector);
    };

    // long time ago
    var longTimeAgo = function() {
      var timeAgo = function(time, ago) {
        return Math.round(time) + ago;
      };
      $('time').each(function(i, e){
        var past = parseInt(e.dataset.time);
        var now = Math.round(new Date().getTime() / 1000);
        var seconds = now - past;
        var ago = seconds / 60;
        // log('time ago', e, past, now, ago);
        var oneHour = 60;
        var oneDay = oneHour * 24;
        // var oneWeek = oneDay * 7;
        var oneMonth = oneDay * 30;
        var oneYear = oneMonth * 12;
        var s = '';
        if(seconds < 60) {
            s = timeAgo(seconds, ' 秒前')
        } else if (ago < oneHour) {
            s = timeAgo(ago, ' 分钟前');
        } else if (ago < oneDay) {
            s = timeAgo(ago/oneHour, ' 小时前');
        } else if (ago < oneMonth) {
            s = timeAgo(ago / oneDay, ' 天前');
        }
        $(e).text(s);
      });
    };

    var chatResponse = function(r) {
        var chat = JSON.parse(r);
        chatStore[chat.channel].push(chat);
        if(chat.channel == currentChannel) {
            insertChatItem(chat);
        }
    };

    var subscribe = function() {
      var sse = new EventSource("/chat/subscribe");
      sse.onmessage = function(e) {
        log(e, e.data);
        chatResponse(e.data);
     };
    };

    var sendMessage = function(){
      var content = $('#id-input-content').val();
      var message = {
        content: content,
        channel: currentChannel,
      };

      var request = {
        url: '/chat/add',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(message),
        success: function(r){
          log('success', r);
        },
        error: function(err) {
          log('error', err);
        }
      };
      $.ajax(request);
    };

    var changeChannel = function(channel) {
        document.title = '聊天室 - ' + channel;
        currentChannel = channel;
    };

    var bindActions = function(){
      $('#id-button-send').on('click', function(){
        if ($('#id-input-content').val().length==0){
          alertify.error('内容不能为空')
          return false
        }
        $("#id-button-send").addClass("disabled");
        sendMessage();
        $('#id-input-content').val('');
        var count = 2;
        var countdown = setInterval(CountDown, 1000);
        function CountDown() {
            $("#id-button-send").addClass("disabled");
            $("#id-button-send").text("稍等"+count+"s");
            $("#id-button-send").css({'background':'#cccccc'})
            if (count == 0) {
                $("#id-button-send").text("发送消息").removeClass("disabled");
                $("#id-button-send").css({'background':'#26a69a'})
                clearInterval(countdown);
            }
            count--;
        }
      });
      // 频道切换
      $('.rc-channel').on('click', function(e){
          e.preventDefault();
          //
          var channel = $(this).text();
          changeChannel(channel);
          // 切换显示
          $('.rc-channel').removeClass('active-channel');
          $(this).addClass('active-channel');
          // reload 信息
          $('#id-div-chats').empty();
          var chats = chatStore[currentChannel];
          insertChats(chats);
      })
    };


    var sendMessageEnter = function () {
        $(document).on('keyup',function(e){
            if(e.keyCode === 13){
                if($('#id-button-send').hasClass('disabled')){
                    alertify.error('操作频繁')
                }else {
                    $('#id-button-send').click()
                }
            }
        });
    };

    var __main = function(){
      subscribe();
      bindActions();
      sendMessageEnter();
      // 选中第一个 channel 作为默认 channel
      $('.rc-channel')[0].click();
      // 更新时间的函数
      setInterval(function () {
          longTimeAgo();
      }, 1000);
    };

    $(document).ready(function(){
      __main();
    });
