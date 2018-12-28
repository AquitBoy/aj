function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$('#form-avatar').submit(function(e){
    e.preventDefault()
     $(this).ajaxSubmit({
        url:'/user/upload_img/',
        type:'post',
        dataType:'json',
        success:function(data){
            if(data.code == 200){
                $("#user-avatar").attr('src','/static/images/'+data.avatar)
            }
        }

    })
})

$('#form-name').submit(function(e){
    e.preventDefault()
     $(this).ajaxSubmit({
        url:'/user/upload_name/',
        type:'post',
        dataType:'json',
        success:function(data){
            alert('保存成功')
        }
    })
})

$(document).ready(function(){
$.ajax({
        url:'/user/get_user/',
        datatype:'json',
        type:'post',
        success:function(data){
            if(data.code == 200){
                if(data.avatar){
                $('#user-avatar').attr('src','/static/images/'+data.avatar)
                }
                $('#user-name').val(data.name)
            }
        },
    })
})