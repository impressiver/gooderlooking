# -*- coding:utf-8 -*-
from flask import g, Blueprint, redirect, session, current_app, url_for
from flask.ext.security import current_user
from datetime import datetime, timedelta
from database import db
from account.oauth import oauth, oauth_authorized

mod = Blueprint('foursquare', __name__, url_prefix='/oauth/foursquare')

foursquare = oauth.remote_app('foursquare',
    base_url = 'https://graph.foursquare.com/',
    request_token_url = None,
    access_token_url = '/oauth/access_token',
    authorize_url = 'https://foursquare.com/dialog/oauth',
    consumer_key = '22100925992',
    consumer_secret = 'd521680c055c030c1d64eee77ed60f78',
    request_token_params = { 'scope': 'email,user_checkins,user_location,user_photos' }
)

@foursquare.tokengetter
def foursquare_token():
    if current_user.is_authenticated():
        service = current_user.service('foursquare')
        if service:
            return service.token, ''


@mod.route('/signin')
def foursquare_signin():
    return foursquare.authorize(callback='http://gooderlooking.com/oauth/foursquare/authorized')


@mod.route('/authorized')
@foursquare.authorized_handler
def foursquare_authorized(resp):
    expires = datetime.utcnow() + timedelta(seconds=long(resp['expires']))
    oauth_authorized(provider='foursquare', token=resp['access_token'], expires=expires)
    
    # Update service with user id and name
    me = foursquare.get('/me')
    current_user.service('foursquare').service_user_id = me.data['id']
    current_user.service('foursquare').screen_name = me.data['name']
    db.session.commit()
    
    return redirect(url_for('account.profile'))