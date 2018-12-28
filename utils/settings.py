"""
author:何凯
date:
"""
import os

DATABASE = {
    'NAME': 'aj',
    'USER': 'root',
    'PASSWORD': '123456',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'ENGINT': 'mysql',
    'DRIVER': 'pymysql'
    }
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,'static')
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
IMAGES_DIR = os.path.join(STATIC_DIR,'images')