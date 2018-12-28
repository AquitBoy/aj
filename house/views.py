"""
author:何凯
date:
"""
import os
from time import strptime
from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, session
from sqlalchemy import and_, or_

from models import Area, Facility, House, db, HouseImage, User, Order
from utils.functions import is_login, is_auth
from utils.settings import IMAGES_DIR

house = Blueprint('house', __name__)


@house.route('/index/', methods = ['GET'])
def index():
    return render_template('index.html')


@house.route('/detail/', methods = ['GET'])
def detail():
    return render_template('detail.html')


@house.route('/search/', methods = ['GET'])
def search():
    return render_template('search.html')


@house.route('/add_house/', methods = ['GET'])
@is_auth
def add_house():
    return render_template('newhouse.html')


@house.route('/get_area/', methods = ['GET'])
def get_area():
    areas = Area.query.all()
    area_name = [area.name for area in areas]
    return jsonify({'area': area_name})


@house.route('/get_facility/', methods = ['GET'])
def get_facility():
    facility = Facility.query.all()
    data = []
    for f in facility:
        name = f.name
        id = f.name
        data.append({'name': name, 'id': id})
    return jsonify({'facility': data})


@house.route('/add_house/', methods = ['POST'])
def add_house_post():
    form = request.form
    # 获取页面数据
    title = form.get('title')
    price = form.get('price')
    area_id = form.get('area_id')
    address = form.get('address')
    room_count = form.get('room_count')
    acreage = form.get('acreage')
    unit = form.get('unit')
    capacity = form.get('capacity')
    beds = form.get('beds')
    deposit = form.get('deposit')
    min_days = form.get('min_days')
    max_days = form.get('max_days')
    facility = form.getlist('facility')
    # 存储数据
    house = House()
    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    house.user_id = session.get('user_id')
    # 添加，提交house到数据库
    house.add_update()
    # 将facility对象加入到fac列表中
    fac = []
    for i in facility:
        fac.append(Facility.query.filter(Facility.name == i).first())
    # 向中间表中添加对象
    house.facilities += fac
    # 提交
    db.session.commit()
    # 获取新加的house的id
    house_id = house.id
    return jsonify({'house_id': house_id})


@house.route('/add_house_image/', methods = ['POST'])
@is_auth
def add_house_image():
    img = request.files.get('house_image')
    path = os.path.join(IMAGES_DIR, img.filename)
    # 保存图片
    img.save(path)
    name = img.filename
    # 获取house的id并将数据插入数据库
    house_id = int(request.form.get('house_id'))
    house = House.query.get(house_id)
    house.index_image_url = name
    # 存储房间的主图片
    house.add_update()
    image = HouseImage()
    image.house_id = house_id
    image.url = name
    image.add_update()
    return jsonify({'img_name': name})


@house.route('/get_detail/', methods = ['POST'])
def get_detail():
    id = request.form.get('id')
    house = House.query.get(id)
    info = house.to_full_dict()
    # 判断是否是本人发布的房源
    user_id = session.get('user_id')
    house_user_id = house.user_id
    is_mine = False
    if user_id == house_user_id:
        is_mine = True
    return jsonify({'house': info, 'is_mine': is_mine})


@house.route('/get_all_houses/', methods = ['GET'])
def get_all_houses():
    houses = House.query.all()
    data = []
    for house in houses:
        house = house.to_dict()
        data.append(house)
    return jsonify({'houses': data})


@house.route('/search/', methods = ['POST'])
def search_post():
    form = request.form
    aid = form.get('aid')
    sd = form.get('sd')
    ed = form.get('ed')
    # 根据地区筛选出house
    if aid:
        houses = House.query.filter(House.area_id == aid)
    else:
        houses = House.query.all()
    area_house_id = {house.id for house in houses}
    # 得到正在使用的house
    orders = Order.query.filter(Order.status.in_(["WAIT_ACCEPT", "WAIT_PAYMENT", "PAID"]))
    # 根据时间来筛选house
    if (sd and ed):
        sd = datetime.strptime(sd, "%Y-%m-%d")
        ed = datetime.strptime(ed, "%Y-%m-%d")
        house_inuse = orders.filter(or_(and_(Order.end_date <= ed, Order.end_date >= sd),and_(Order.begin_date <= ed, Order.begin_date >= sd)))
        hosue_inuse_id = set([house.house_id for house in house_inuse])
    else:
        # 如果开始时间，结束时间没填全，就不做筛选
        hosue_inuse_id = set()

    house_can_order_id = list(area_house_id-hosue_inuse_id)
    if not house_can_order_id:
        return jsonify({'code':1001,'msg':'没有房子'})

    # 封装数据
    data = []
    for id in house_can_order_id:
        house = houses.filter(House.id == id).first()
        msg = house.to_full_dict()
        # 入住人数
        num = len(house.orders)
        msg['num']=num
        # 创建时间
        create_time = house.create_time
        msg['create_time']=create_time
        data.append(msg)
    # 排序
    sort_key = form.get('sort_key')
    if sort_key == 'num':
        # 根据入住人数
        data = sorted(data,key = lambda msg:msg['num'],reverse = True)
    elif sort_key == 'price_asc':
        # 根据价格升序
        data = sorted(data,key = lambda msg:msg['price'])
    elif sort_key == 'price_desc':
        # 根据价格降序
        data = sorted(data,key = lambda msg:msg['price'],reverse = True)
    else:
        # 根据上线时间(默认)
        data = sorted(data, key = lambda msg: msg['create_time'], reverse = True)
    return jsonify({'code':200,'houses':data})
