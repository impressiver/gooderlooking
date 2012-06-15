# -*- coding:utf-8 -*-
from flask import g, Blueprint, redirect, session, current_app, url_for
from flask.ext.security import current_user
from datetime import datetime, timedelta
from database import db
from account.oauth import oauth, oauth_authorized

mod = Blueprint('facebook', __name__, url_prefix='/oauth/facebook')

facebook = oauth.remote_app('facebook',
    base_url = 'https://graph.facebook.com/',
    request_token_url = None,
    access_token_url = '/oauth/access_token',
    authorize_url = 'https://facebook.com/dialog/oauth',
    consumer_key = '22100925992',
    consumer_secret = 'd521680c055c030c1d64eee77ed60f78',
    request_token_params = { 'scope': 'email,user_checkins,user_location,user_photos' }
)

@facebook.tokengetter
def facebook_token():
    if current_user.is_authenticated():
        service = current_user.service('facebook')
        if service:
            return service.token, ''


@mod.route('/signin')
def facebook_signin():
    return facebook.authorize(callback='http://gooderlooking.com/oauth/facebook/authorized')


@mod.route('/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    expires = datetime.utcnow() + timedelta(seconds=long(resp['expires']))
    oauth_authorized(provider='facebook', token=resp['access_token'], expires=expires)
    
    # Update service with user id and name
    me = facebook.get('/me')
    current_user.service('facebook').service_user_id = me.data['id']
    current_user.service('facebook').screen_name = me.data['name']
    db.session.commit()
    
    return redirect(url_for('account.profile'))