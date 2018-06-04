// 解析url中的查询字符串
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

// 关注取消关注
$(function(){
           // 关注当前新闻作者
    $(".focus").click(function () {
        $.post('/userfollow',{
            'csrf_token':$('#csrf_token').val(),
            'action':1,
            'follow_user_id':$('#follow_user_id').val()
        },function (data) {
            if (data.result==1){
                $('.login_btn').click();
            }else if (data.result==2){
                $('.focus').hide();
                $('.focused').show();
            }
        })
    });

    // 取消关注当前新闻作者
    $(".focused").click(function () {
        $.post('/userfollow',{
            'csrf_token':$('#csrf_token').val(),
            'action':2,
            'follow_user_id':$('#follow_user_id').val()
        },function (data) {
            if (data.result==1){
                ('.login_btn').click();
            }else if (data.result==2){
                $('.focus').show();
                $('.focused').hide();
            }
        })
    })
});

