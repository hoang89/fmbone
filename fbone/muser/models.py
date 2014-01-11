from flask.ext.social.core import Social
from mongoengine.queryset.visitor import Q

__author__ = 'hoangnn'

from flask.ext.mongoengine import *
from mongoengine.fields import *
from mongoengine.document import *
from constants import *
from ..utils import *
from bson import ObjectId
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class Address(EmbeddedDocument):
    country = StringField()
    city = StringField()
    sub = StringField()

class MUserDetail(EmbeddedDocument):
    age = IntField()
    phone = StringField()
    url = URLField()
    address = EmbeddedDocumentField(Address)
    sex_code = IntField()
    birthday = DateTimeField()
    modified = DateTimeField()
    first_name = StringField()
    last_name = StringField()
    bio = StringField()

    @property
    def sex(self):
        return SEX_TYPE.get(self.sex_code)

    def save(self,*args, **kwargs):
        self.modified = datetime.datetime.utcnow()
        return super(MUserDetail, self).save(*args, **kwargs)


class MUser(Document, UserMixin):
    username = StringField()
    email = EmailField()
    password = StringField()
    openid = StringField()
    activation_code = StringField()
    avatar = StringField()
    role_code = IntField(default=USER)
    detail = EmbeddedDocumentField(MUserDetail)
    created = DateTimeField()
    modified = DateTimeField()
    password_hash = StringField()


    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    @classmethod
    def get_by_id(cls, _id):
        try:
            user = cls.objects(id=ObjectId(_id)).first()
            return user
        except Exception as e:
            return None
    @classmethod
    def get_by_username(cls, username):
        try:
            user = cls.objects(username=username).first()
            return user
        except Exception as e:
            return None

    @classmethod
    def get_by_email(cls, email):
        try:
            user = cls.objects(email=email).first()
            return user
        except Exception as e:
            return None

    def set_hash_password(self, password):
        if password:
            self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, login, password):
        user = cls.objects.filter(Q(username=login) | Q(email=login)).first()
        if user:
            auth = check_password_hash(user.password_hash, password)
            return user, auth
        return None, False

    def save(self,*args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()
        if self.password:
            self.password = generate_password_hash(self.password)
        return super(MUser, self).save(*args, **kwargs)