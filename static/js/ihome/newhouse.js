function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.get('/house/get_area/',function(data){
        var str1 = ''
        for(i=0;i<data.area.length;i++){
            str1 += '<option value="1">'+data.area[i]+'</option>'
        }
        $('#area-id').html(str1)
    })

    $.get('/house/get_facility/',function(data){
            var str1 = ''
            for(i=0;i<data.facility.length;i++){
                str1 += '<li><div class="checkbox"><label><input type="checkbox" name="facility" value="'+data.facility[i].id+'">'+data.facility[i].name+'</label></div></li>'
            }
            $('.house-facility-list').html(str1)
        })
})

$('#form-house-info').submit(function(e){
    e.preventDefault()
    $(this).ajaxSubmit({
        url:'/house/add_house/',
        datatype:'json',
        type:'post',
        success:function(data){
           $('#form-house-info').hide()
           $('#form-house-image').show()
           $('#house-id').val(data.house_id)
        }
    })
})

$('#form-house-image').submit(function(e){
    e.preventDefault()
    $(this).ajaxSubmit({
        url:'/house/add_house_image/',
        datatype:'json',
        type:'post',
        success:function(data){
           $('.house-image-cons').append('<img src="/static/images/'+data.img_name+'">')
        }
    })
})