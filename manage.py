# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from fbone import create_app
from fbone.extensions import db
from fbone.user import User, UserDetail, ADMIN, ACTIVE
from fbone.utils import MALE
from fbone.muser.models import MUser, MUserDetail, Address


app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run()


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
            name=u'admin',
            email=u'admin@example.com',
            password=u'123456',
            role_code=ADMIN,
            status_code=ACTIVE,
            user_detail=UserDetail(
                sex_code=MALE,
                age=10,
                url=u'http://admin.example.com',
                deposit=100.00,
                location=u'Hangzhou',
                bio=u'admin Guy is ... hmm ... just a admin guy.'))
    db.session.add(admin)
    db.session.commit()
    create_user()

def create_user():
    MUser.drop_collection()
    user = MUser()
    detail = MUserDetail()
    address = Address()
    address.country = 'Viet Nam'
    address.city = 'Ha Noi'
    address.sub = 'Minh  khai - Hoang Mai'
    detail.address = address
    detail.age = 24
    user.detail = detail
    user.username = 'hoangnn'
    user.email = 'hoangnn@gmail.com'
    user.set_hash_password('123456')
    user.save()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
