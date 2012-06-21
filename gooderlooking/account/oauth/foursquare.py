# -*- coding:utf-8 -*-
from flask import g, Blueprint, redirect, session, current_app, url_for
from flask.ext.security import current_user
from database import db
from urlparse import urljoin
from account.oauth import oauth, oauth_authorized
import json

mod = Blueprint('foursquare', __name__, url_prefix='/oauth/foursquare')


endpoints = {
    'base_url': 'https://api.foursquare.com/v2/'
}

def _get_endpoint(*args):
    return urljoin(endpoints['base_url'], *args)


foursquare = oauth.remote_app('foursquare',
    base_url = 'https://foursquare.com',
    authorize_url = '/oauth2/authenticate',
    request_token_url = None,
    request_token_params = {'response_type': 'code'},
    access_token_url = '/oauth2/access_token',
    access_token_params = {'grant_type': 'authorization_code'},
    consumer_key = 'NM2YNOFAMFFMTETI0VHPWAR1XUWN52FMCGLOILLN1R0GD0PG',
    consumer_secret = 'GHUOD40DMN5AVGQ25JZXG4MIZ04LTBY0YKZY1IB0BZ451DCC'
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
    current_app.logger.debug(resp)
    
    oauth_authorized(provider='foursquare', token=resp['access_token'])
    
    # Update service with user id and name
    current_app.logger.debug(_get_endpoint('users/self'))
    info = foursquare.get(_get_endpoint('users/self'))
    current_app.logger.debug(json.dumps(info.data))
    
    current_user.service('foursquare').service_user_id = info.data['response']['user']['id']
    current_user.service('foursquare').first_name = info.data['response']['user']['firstName']
    current_user.service('foursquare').last_name = info.data['response']['user']['lastName']
    
    if info.data['response']['user']['firstName'] and not current_user.first_name:
        current_user.first_name = info.data['response']['user']['firstName']
        current_user.last_name = info.data['response']['user']['lastName']
        
    if info.data['response']['user']['homeCity'] and not current_user.city:
        current_user.city = info.data['response']['user']['homeCity']
        
    db.session.commit()
    
    return redirect(url_for('account.profile'))