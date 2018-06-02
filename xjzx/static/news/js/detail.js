function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function(){
    // 定义控制新闻评论的vue对象
    vue_comment_list = new Vue({
         el: '.comment_list_con',
         delimiters: ['[[', ']]'],//将语法中的{{换成[[，将}}换成]]
         data: {
             comment_list: []
         }
     });
    show_comments();
    // 收藏
    $(".collection").click(function () {
        $.post('/collection/' + $('#news_id').val(),
            {'csrf_token':$('#csrf_token').val()},
        function (data) {
            if ($('#user').html()){
                if (data.result==4){
                $('.collection').hide();
                $('.collected').show();
                }
            }else {
                $('.login_btn').click();
            }

        })
       
    });

    // 取消收藏
    $(".collected").click(function () {
         $.post('/collection/' + $('#news_id').val(),
            {'csrf_token':$('#csrf_token').val(),
            action:1},
        function (data) {
            if ($('#user').html()){
                if (data.result==4){
                $('.collection').show();
                $('.collected').hide();
                }else if(data.result==6){
                    alert('收藏失败！')
                }

            }else {
                $('.login_btn').click();
            }

        })
     
    });

        // 评论提交
    $(".comment_form").submit(function (e) {
        e.preventDefault();
        $.post('/comment/add',
            {'csrf_token':$('#csrf_token').val(),
            'msg':$('.comment_input').val(),
            'news_id':$('#news_id').val()},
        function (data) {
            if ($('#user').html()){
                if (data.result==4){
                    $('.comment_count').html(data.comment_count + '条评论');
                    $('.comment').html(data.comment_count);
                    $('.comment_input').val('');
                    show_comments();
                }else if(data.result==6){
                    alert('评论失败！')
                }
            }else{
                $('.login_btn').click();
            }
        })
    });

    $('.comment_list_con').delegate('a,input','click',function(){

        var sHandler = $(this).prop('class');

        if(sHandler.indexOf('comment_reply')>=0)
        {
            $(this).next().toggle();
        }

        if(sHandler.indexOf('reply_cancel')>=0)
        {
            $(this).parent().toggle();
        }

        if(sHandler.indexOf('comment_up')>=0)
        {
            var $this = $(this);
            if(sHandler.indexOf('has_comment_up')>=0)
            {
                // 如果当前该评论已经是点赞状态，再次点击会进行到此代码块内，代表要取消点赞
                $this.removeClass('has_comment_up')
            }else {
                $this.addClass('has_comment_up')
            }
        }

        if(sHandler.indexOf('reply_sub')>=0)
        {
            alert('回复评论')
        }
    });

        // 关注当前新闻作者
    $(".focus").click(function () {

    });

    // 取消关注当前新闻作者
    $(".focused").click(function () {

    })
});

function show_comments() {
    $.get('/comment/show',
        {'news_id':$('#news_id').val()},
        function (data) {
        if (data.result==2){
            vue_comment_list.comment_list = data.comment_list
        }
    })
}