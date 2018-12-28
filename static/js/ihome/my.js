function logout() {
    $.get("/user/logout/", function(data){
        if (data.code==200) {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function(){
$.ajax({
        url:'/user/get_user/',
        data:{},
        datatype:'json',
        type:'post',
        success:function(data){
            if(data.code == 200){
                $('#user-mobile').html(data.phone)
                $('#user-name').html(data.name)
                if(data.avatar){
                    $('#user-avatar').attr('src','/static/images/'+data.avatar)
                }
            }
        },
        error:function(){
            alert('请求失败，我们会尽快处理')
        }
    })
})
