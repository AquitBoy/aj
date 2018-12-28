$(document).ready(function(){
    $.ajax({
        url:'/user/get_user/',
        datatype:'json',
        type:'post',
        success:function(data){
            if(data.id_name){
                $(".auth-warn").hide();
                $("#houses-list").show();
                $.get('/user/get_myhouse/',function(data){
                    if(data.code == 200){
                        var str = ''
                        for(i=0;i<data.houses.length;i++){
                            var id = data.houses[i].id
                            var title = data.houses[i].title
                            var price = data.houses[i].price
                            var image = data.houses[i].image
                            var area = data.houses[i].area
                            var create_time = data.houses[i].create_time
                            str += '<li><a href="/house/detail/?id='+id+'"><div class="house-title"><h3>房屋ID:'+(i+1)+' —— '+title+'</h3></div><div class="house-content"><img src="/static/images/'+image+'"><div class="house-text"><ul><li>位于：'+area+'</li><li>价格：￥'+price+'/晚</li><li>发布时间：'+create_time+'</li></ul></div></div></a></li>'
                        }
                        $("#myhouse_list").html(str)
                    }
                 })
            }
            else{
                $(".auth-warn").show();
                $("#houses-list").hide();
            }
        },
    })


})