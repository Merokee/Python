function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    var $a = $('.edit');
    var $pop = $('.pop_con');
    var $cancel = $('.cancel');
    var $confirm = $('.confirm');
    var $error = $('.error_tip');
    var $input = $('.input_txt3');
    var sHandler = 'edit';
    var sId = 0;
    vue_category_list = new Vue({
        el: '.common_table',
        delimiters: ['[[', ']]'],
        data: {
            category_list: []
        },
        methods: {
            add: function () {
                sHandler = 'add';
                $pop.find('h3').html('新增分类');
                $input.val('');
                $pop.show();
            }, edit: function (event) {
                $this = $(event.target);
                sHandler = 'edit';
                sId = $this.parent().siblings().eq(0).html();
                $pop.find('h3').html('修改分类');
                $pop.find('.input_txt3').val($this.parent().prev().html());
                $pop.show();
            }
        }
    });
    get_category_list();

    $a.click(function () {

    });

    $cancel.click(function () {
        $pop.hide();
        $error.hide();
    });

    $input.click(function () {
        $error.hide();
    });

    $confirm.click(function () {
        if (sHandler == 'edit') {
            var sVal = $input.val();
            if (sVal == '') {
                $error.html('输入框不能为空').show();
                return;
            } else {
                $.post('/admin/change_category', {
                    'csrf_token': $('#csrf_token').val(),
                    'name': sVal,
                    'id': sId
                }, function (data) {
                    if (data.result == 1) {
                        $cancel.click();
                        get_category_list();
                    }else if(data.result==0){
                        $error.html('输入框不能为空').show();
                    }else if(data.reslut==-1){
                        $error.html('类名已存在！').show();
                    }
                })
            }
        }
        else {
            var sVal = $input.val();
            if (sVal == '') {
                $error.html('输入框不能为空').show();
                return;
            } else {
                $.post('/admin/add_category',
                    {
                        'csrf_token': $('#csrf_token').val(),
                        'name': sVal
                    },
                    function (data) {
                        if (data.result == 1) {
                            $cancel.click();
                            get_category_list();
                        } else if (data.result == 0) {
                            $error.html('输入框不能为空').show();
                        } else if (data.result == 1) {
                            $error.html('类名已存在！').show();
                        }
                    })
            }
        }

    })
});
function get_category_list() {
    $.get('/admin/news_type_json',
        function (data) {
            vue_category_list.category_list = data.category_list;
        });
}