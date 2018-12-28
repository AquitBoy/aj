function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$('#form-auth').submit(function(e){
    e.preventDefault()
     $(this).ajaxSubmit({
        url:'/user/auth/',
        type:'post',
        dataType:'json',
        success:function(data){
            if(data.code == 200){
                $("#real-name").attr('disabled','disabled')
                $("#id-card").attr('disabled','disabled')
                $(".btn-success").hide()
                $(".popup_con").css('display','block')
                $('.error-msg').hide()

            }
            else{
                $('.error-msg').html(data.error)
                $('.error-msg').show()
            }
        }

    })
})

$(document).ready(function(){
$.ajax({
        url:'/user/get_user/',
        datatype:'json',
        type:'post',
        success:function(data){
            if(data.id_name){
                $("#real-name").attr('disabled','disabled')
                $("#real-name").val(data.id_name)
                $("#id-card").attr('disabled','disabled')
                $("#id-card").val(data.id_card)
                $(".btn-success").hide()
            }
        },
    })
})



