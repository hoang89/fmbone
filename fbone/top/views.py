from datetime import datetime
from flask.ext.restful.representations import json
from sqlalchemy.orm.session import _SessionClassMethods

__author__ = 'hoangnn'

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask.ext.login import current_user, login_required, login_user, logout_user
from forms import LoginForm, SignupForm
from ..muser.models import MUser, MUserDetail
from flask.ext.babel import gettext as _
from flask.globals import current_app
from fbone.extensions import oauth
from services import TopService
import time

top = Blueprint('top', __name__, url_prefix='/top')
FACEBOOK_APP_ID = '174930302670618',
FACEBOOK_APP_SECRET = 'abdbf2f9b4e183f7f77a2040ec476100'

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'})

@top.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('muser.index'))
    return render_template('top/index.html')

@top.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('top.index'))
    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))
    if form.validate_on_submit():
        user, authenticated = MUser.authenticate(form.login.data, form.password.data)
        if user and authenticated:
            remember = request.form.get('remember') == 'y'
            if login_user(user=user, remember=remember):
                flash(_('Logged in'), 'success')
            return redirect(form.next.data or url_for('top.index'))
        else:
            flash(_('Sorry, invalid login'), 'danger')

    return render_template('top/login.html', form=form)

@top.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('top.index'))
    form = SignupForm(next=request.args.get('next', None))
    if form.validate_on_submit():
        user = MUser()
        user_detail = MUserDetail()
        user.detail = user_detail
        user.email = form.email.data
        user.username = form.username.data
        user.set_hash_password(form.password.data)
        user.save()
        if login_user(user):
            flash(_('Suceess signup'), 'success')
            return redirect(form.next.data or url_for('top.index'))

    return render_template('top/signup.html', form=form)

@top.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(_('Logged out'), 'success')
    return redirect(url_for('top.index'))

@top.route('/fb', methods=['GET', 'POST'])
def fb():
    return facebook.authorize(callback=url_for('top.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@top.route('/fb/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = TopService.fb_register(me.data)
    if login_user(user):
        flash(_('Suceess signup'), 'success')
    return redirect(url_for('top.index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
