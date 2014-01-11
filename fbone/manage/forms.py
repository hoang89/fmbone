__author__ = 'hoangnn'
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from wtforms import (ValidationError, HiddenField, TextField, HiddenField,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField)
from wtforms.validators import (Required, Length, EqualTo, Email, NumberRange,
        URL, AnyOf, Optional)
from flask.ext.login import current_user

from ..user import User
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, AGE_MIN, AGE_MAX, DEPOSIT_MIN, DEPOSIT_MAX
from ..utils import allowed_file, ALLOWED_AVATAR_EXTENSIONS
from ..utils import SEX_TYPE

class ProfileForm(Form):
    multipart = True
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()])
    # Don't use the same name as model because we are going to use populate_obj().
    avatar_file = FileField(u"Avatar", [Optional()])
    sex_code = RadioField(u"Sex", [AnyOf([str(val) for val in SEX_TYPE.keys()])], choices=[(str(val), label) for val, label in SEX_TYPE.items()])
    age = IntegerField(u'Age', [Optional(), NumberRange(AGE_MIN, AGE_MAX)])
    phone = TelField(u'Phone', [Length(max=64)])
    url = URLField(u'URL', [Optional(), URL()])
    country = TextField(u'Country', [Length(max=64)])
    city = TextField(u'City', [Length(max=64)])
    sub = TextField(u'Detail Localtion', [Length(max=64)])
    submit = SubmitField(u'Save')

    def validate_avatar_file(form, field):
        if field.data and not allowed_file(field.data.filename):
            raise ValidationError("Please upload files with extensions: %s" % "/".join(ALLOWED_AVATAR_EXTENSIONS))
