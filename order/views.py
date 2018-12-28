"""
author:何凯
date:
"""
from flask import Blueprint, render_template, request, jsonify, session
from time import strftime,strptime
from datetime import datetime

from sqlalchemy import or_, and_

from models import House, Order
from utils.functions import is_auth

order = Blueprint('order',__name__)


@order.route('/booking/',methods=['GET'])
def booking_get():
    return render_template('booking.html')


@order.route('/booking/',methods=['POST'])
def booking_post():
    pass


@order.route('/get_booking_house/',methods = ['POST'])
def get_booking_house():
    id = request.form.get('id')
    house = House.query.get(id)
    # 判断是否是本人发布的房源
    user_id = session.get('user_id')
    house_user_id = house.user_id
    is_mine = False
    if user_id == house_user_id:
        is_mine = True
    info = [house.to_dict()]
    return jsonify({'code':200,'houses':info,'is_mine':is_mine})


@order.route('/make_order/',methods = ['POST'])
@is_auth
def make_order():
    data = request.form
    id = data.get('id')
    sd = data.get('start_date')
    ed = data.get('end_date')
    # 对订单时间进行验证
    # 得到正在使用的house
    orders = Order.query.filter(Order.status.in_(["WAIT_ACCEPT", "WAIT_PAYMENT", "PAID"]))
    # 根据时间来筛选house
    if (sd and ed):
        start_date = datetime.strptime(sd, "%Y-%m-%d")
        end_date = datetime.strptime(ed, "%Y-%m-%d")
        house_inuse = orders.filter(
            or_(and_(Order.end_date <= end_date, Order.end_date >= start_date), and_(Order.begin_date <= end_date, Order.begin_date >= start_date)))
        hosue_inuse_id = [house.house_id for house in house_inuse]
    else:
        # 如果开始时间，结束时间没填全，返回错误
        return jsonify({'code':1001,'msg':'参数不全'})
    if id in hosue_inuse_id:
        return jsonify({'code': 1001, 'msg': '房子在使用'})

    # 创建订单
    order = Order()
    order.user_id = session.get('user_id')
    order.house_id = id
    order.begin_date = start_date
    order.end_date = end_date
    start_date = strptime(sd,'%Y-%m-%d')
    end_date = strptime(ed,'%Y-%m-%d')
    start_date = datetime(start_date[0],start_date[1],start_date[2])
    end_date = datetime(end_date[0],end_date[1],end_date[2])
    order.days = (end_date-start_date).days+1
    order.house_price = House.query.get(id).price
    order.amount = order.days*order.house_price
    order.add_update()
    return jsonify({'code':200,'amount':order.amount})


