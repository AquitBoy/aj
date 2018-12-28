"""
author:何凯
date:
"""
from flask import Flask
from house.views import house
from models import db
from order.views import order
from user.views import user
from utils.config import Conf
from utils.settings import STATIC_DIR, TEMPLATE_DIR


def create_app():
    app = Flask(__name__,
                static_folder = STATIC_DIR,
                template_folder = TEMPLATE_DIR)
    app.config.from_object(Conf)
    app.register_blueprint(blueprint = user,url_prefix = '/user')
    app.register_blueprint(blueprint = order,url_prefix = '/order')
    app.register_blueprint(blueprint = house,url_prefix = '/house')
    db.init_app(app)
    return app
