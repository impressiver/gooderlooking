# -*- coding:utf-8 -*-
from flask import (Blueprint, current_app, request, g, session, redirect, flash, render_template, url_for)
from flask.ext.login import login_user, logout_user
from flask.ext.principal import Identity, identity_changed
from flask.ext.security import current_user, login_required
from flask.ext.security.utils import get_post_login_redirect
from flask.ext.security.exceptions import UserNotFoundError, BadCredentialsError
from flaskext.openid import OpenID

mod = Blueprint('openid', __name__, url_prefix='/openid')

oid = OpenID()

def init_blueprint(state):
    app = state.app
    oid.init_app(app)
    

def _do_login(user, remember=True):
    if login_user(user, remember):
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        current_app.logger.debug('User %s logged in' % user)
        return True
        
    current_app.logger.debug('User %s failed login' % user)
    return False
        
        
@mod.before_request
def lookup_current_user():
    if not current_user.is_authenticated() and 'openid' in session:
        try:
            user = current_app.security.auth_provider.authenticate_openid(session['openid'])
            if user:
                _do_login(user)
        except BadCredentialsError:
            pass


@mod.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if current_user.is_authenticated():
        current_app.logger.debug("Current user %s", current_user)
        return redirect(oid.get_next_url())
        
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email', 'fullname', 'nickname'])
            
    return render_template('login.html', next=oid.get_next_url(), error=oid.fetch_error())


@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    
    current_app.logger.debug("User: %s", current_user)
    
    try:
        user = current_app.security.auth_provider.authenticate_openid(session['openid'])
        if user and _do_login(user):
            flash(u'Successfully signed in')
            return redirect(get_post_login_redirect())
    except BadCredentialsError, UserNotFoundError:
        if current_user.get_id() is not None:
            # Looks like the openid token changed... not sure how, so we'll wipe it and start over
            current_user['openid'] = None
            security.datastore._save_model(current_user)
            
            return redirect(url_for('login'))
        
    return redirect(url_for('account.create_profile', next=oid.get_next_url(), name=resp.fullname or resp.name or resp.nickname, email=resp.email))
    

@mod.route('/logout')
def logout():
    session.pop('openid', None)
    logout_user()
    
    flash(u'You were signed out')
    return redirect(oid.get_next_url())
    
    
mod.record(init_blueprint)