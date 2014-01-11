# -*- coding: utf-8 -*-
from flask.ext.oauth import OAuth

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.mongoengine import MongoEngine
mongo = MongoEngine()

from flask.ext.mail import Mail
mail = Mail()

from flask.ext.cache import Cache
cache = Cache()

from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.openid import OpenID
oid = OpenID()

oauth = OAuth()
