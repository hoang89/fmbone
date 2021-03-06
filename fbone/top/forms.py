__author__ = 'hoangnn'
from flask import Markup

from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from wtforms.validators import Required, Length, EqualTo, Email
from flask.ext.wtf.html5 import EmailField

from ..muser.models import MUser
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)

class LoginForm(Form):
    next = HiddenField()
    login = TextField(u'Username or email', [Required()])
    password = PasswordField('Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class SignupForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()],
            description=u"What's your email address?")
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s characters or more! Be tricky.' % PASSWORD_LEN_MIN)
    username = TextField(u'Choose your username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    agree = BooleanField(u'Agree to the ' +
        Markup('<a target="blank" href="/terms">Terms of Service</a>'), [Required()])
    submit = SubmitField('Sign up')

    def validate_username(self, field):
        if MUser.get_by_username(field.data):
            raise ValidationError(u'This username is taken')

    def validate_email(self, field):
        if MUser.get_by_email(field.data):
            raise ValidationError(u'This email is taken')

