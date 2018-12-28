function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    $(".book-house").show();

    id = location.search.split('=')[1]
    $.ajax({
        url:'/house/get_detail/',
        datatype:'json',
        type:'post',
        data:{'id':id},
        success:function(data){
            house = data.house
            title = house.title
            user_avatar = house.user_avatar
            user_name=house.user_name
            address = house.address
            room_count = house.room_count
            acreage = house.acreage
            unit = house.unit
            capacity = house.capacity
            beds = house.beds
            deposit = house.deposit
            min_days = house.min_days
            max_days = house.max_days
            images = house.images
            facilities = house.facilities
            order_count  = house.order_count
            price = house.price
//            添加轮播图片
            for(i=0;i<images.length;i++){
                $('.swiper-wrapper').append('<li class="swiper-slide"><img src="/static/images/'+images[i]+'"></li>')
            }
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })
            $('.house-price span').html(price)
            $('.house-title').html(title)
            $('.landlord-pic').html('<img src="/static/images/'+user_avatar+'">')
            $('.landlord-name span').html(user_name)
            $('#house_address').html(address)
            $('#house_info').append('<h3>出租'+room_count+'间</h3>')
            $('#house_info').append('<p>房屋面积:'+acreage+'平米</p>')
            $('#house_info').append('<p>房屋户型:'+unit+'</p>')
            $('#house_capacity').append('<h3>宜住'+capacity+'人</h3>')
            $('#house_beds').append('<p>'+beds+'</p>')
            $('#house_deposit').html(deposit)
            $('#house_min_days').html(min_days)
            $('#house_max_days').html(max_days)
            for(i=0;i<facilities.length;i++){
                $('.house-facility-list').append('<li><span class="'+facilities[i].css+'"></span>'+facilities[i].name+'</li>')
            }
            if(data.is_mine){
                $('.book-house').hide()
            }
        }
    })
    $('.book-house').click(function(e){
        e.preventDefault()
        location.href = '/order/booking/?id='+id
    })
})