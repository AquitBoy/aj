"""
author:何凯
date:
"""
import os
import random
import re

from flask import Blueprint, render_template, jsonify, session, url_for, request, redirect

from models import User, House, Order, db
from utils.functions import is_login, check_idcard, is_auth
from utils.settings import IMAGES_DIR
from utils.status_code import *

user = Blueprint('user', __name__)


@user.route('/register/', methods = ['GET'])
def register_get():
    return render_template('register.html')


@user.route('/register/', methods = ['POST'])
def register_post():
    phone = request.form.get('phone')
    imagecode = request.form.get('imagecode')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    img_code = session.get('img_code')
    if not all([phone, imagecode, password, password2]):
        # 判断所有字段中是否有空
        return jsonify({'empty': FIELD_IS_EMPTY})
    error = {}
    # 手机号验证
    ret = re.match(r"^1[35678]\d{9}$", phone)
    if not ret:
        error['phone'] = USER_PHONE_ERROR
    # 图片验证码验证
    if imagecode != img_code:
        error['imagecode'] = IMG_CODE_ERROR
    # 密码位数验证
    if len(password) < 6:
        error['password_less'] = PASSWORD_LESS
    # 两次密码是否相同
    if password != password2:
        error['password_different'] = TWO_PASSWORD_DIFFERENT
    # 如果有错，返回错误信息
    if error:
        return jsonify(error)
    # 没错返回登陆页面，并存储用户数据
    new_user = User()
    new_user.phone = phone
    new_user.password = password
    new_user.add_update()
    return jsonify({'code':200})


@user.route('/get_img_code/', methods = ['GET'])
def get_img_code():
    img_codes = '1234567890qwertyuiopalwskdjfhgmzxcvbn'
    img_code = ''
    for _ in range(4):
        img_code += random.choice(img_codes)
    session['img_code'] = img_code
    return jsonify({'code': 200, 'data': img_code})


@user.route('/login/', methods = ['GET'])
def login_get():
    return render_template('login.html')


@user.route('/login/', methods = ['POST'])
def login_post():
    phone = request.form.get('mobile')
    password = request.form.get('password')
    user = User.query.filter(User.phone == phone).first()
    if user :
        if user.check_pwd(password):
            session['user_id'] = user.id
            return jsonify({'code':200})
    return jsonify({'error':'请输入正确的电话号码和密码'})


@user.route('/my/',methods = ['GET'])
@is_login
def my():
    return render_template('my.html')


@user.route('/get_user/',methods=['POST'])
def get_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'code':1001})
    user = User.query.get(user_id)
    avatar =user.avatar
    id_name = user.id_name
    id_card = user.id_card
    if not user.name:
        user.name = user.phone
    return jsonify({'code':200,'id_name':id_name,'id_card':id_card,'phone':user.phone,'name':user.name,'avatar':avatar})


@user.route('/auth/',methods = ['GET'])
@is_login
def auth_get():
    return render_template('auth.html')


@user.route('/auth/',methods = ['POST'])
@is_login
def auth_post():
    # 实名认证
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    # 验证name,id_card
    if not all([real_name,id_card]):
        return jsonify({'error':FIELD_IS_EMPTY})
    # 验证唯一性

    regex_name = r'[\u4E00-\u9FA5]{2,}'
    if not re.match(regex_name,real_name):
        return jsonify({'error':NOT_CORRENT_NAME})
    error = check_idcard(id_card)
    if error != '验证通过!':
        return jsonify({'error':error})
    # 验证成功
    user_id = session['user_id']
    user = User.query.get(user_id)
    user.id_name = real_name
    user.id_card = id_card
    user.add_update()

    return jsonify({'code':200})


@user.route('/profile/',methods = ['GET'])
@is_login
def profile_get():
    return render_template('profile.html')
# avatar

@user.route('/upload_img/',methods = ['POST'])
@is_login
def upload_img():
    # 获取图片并保存
    icon = request.files.get('avatar')
    path = os.path.join(IMAGES_DIR,icon.filename)
    icon.save(path)
    # 保存到数据库
    user_id = session['user_id']
    user = User.query.get(user_id)
    user.avatar = icon.filename
    user.add_update()
    return jsonify({'code':200,'avatar':icon.filename})


@user.route('/upload_name/',methods = ['POST'])
@is_login
def upload_name():
    name= request.form.get('name')
    user_id = session['user_id']
    user = User.query.get(user_id)
    user.name = name
    user.add_update()
    return jsonify({'code':200,'name':name})


@user.route('/logout/',methods=['GET'])
@is_login
def logout():
    session.clear()
    return jsonify({'code':200})


@user.route('/myhouse/',methods = ['GET'])
@is_login
def my_house():
    return render_template('myhouse.html')

@user.route('/get_myhouse/',methods=['GET'])
@is_login
def get_myhouse():
    user_id = session.get('user_id')
    houses = House.query.filter(House.user_id == user_id).all()
    data = []
    if houses :
        for house in houses:
            data.append(house.to_dict())
        return jsonify({'code':200,'houses':data})
    return jsonify({'code':IS_NULL,})


@user.route('/my_orders/',methods = ['GET'])
@is_auth
def my_orders():
    return render_template('orders.html')


@user.route('/get_myorders/',methods = ['GET'])
@is_auth
def get_myorders():
    user_id = session.get('user_id')
    orders = Order.query.filter(Order.user_id == user_id).order_by('-create_time').all()
    data = []
    for order in orders:
        order = order.to_dict()
        comment = order['comment']
        if str(comment).startswith('REJECTED'):
            order['comment']=''
            order['rejected']=comment[8:]
        data.append(order)

    return jsonify({'code':200,'orders':data})



@user.route('/my_lorders/',methods=['GET'])
@is_auth
def my_lorders():
    return render_template('lorders.html')


@user.route('/get_mylorders/',methods=['GET'])
def get_mylorders():
    user_id = session.get('user_id')
    houses = House.query.filter(House.user_id == user_id).all()
    orders = [house.orders for house in houses]
    my_lorders = []
    for order in orders:
        my_lorders += order
    # 注意列表中的为对象，还要将它的数据进行处理
    if my_lorders:
        my_lorders = [order.to_dict() for order in my_lorders]
        my_lorders = sorted(my_lorders,key=lambda my_order:my_order['order_id'],reverse=True)

    return jsonify({'code': 200, 'orders': my_lorders})