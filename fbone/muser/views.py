__author__ = 'hoangnn'
from flask import Blueprint, render_template
from flask.ext.login import login_required, current_user

muser = Blueprint('muser', __name__, url_prefix='/muser')

@muser.route('/')
@login_required
def index():
    return render_template('muser/index.html', user=current_user)
