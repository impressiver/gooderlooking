# -*- coding:utf-8 -*-
from flask import g, Blueprint, redirect, session, current_app, url_for
from flask.ext.security import current_user
from database import db
from account.oauth import oauth, oauth_authorized
import json

mod = Blueprint('google', __name__, url_prefix='/oauth/google')

endpoints = {
    'userinfo': 'https://www.googleapis.com/oauth2/v1/userinfo'
}

google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/picasa',
                        'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key='841793997164.apps.googleusercontent.com',
    consumer_secret='fHft78BaxwOhARYTXriYhGOY'
)

@google.tokengetter
def google_token():
    if current_user.is_authenticated():
        service = current_user.service('google')
        if service:
            return service.token, ''


@mod.route('/signin')
def google_signin():
    return google.authorize(callback='http://gooderlooking.com/oauth/google/authorized')


@mod.route('/authorized')
@google.authorized_handler
def google_authorized(resp):
    current_app.logger.debug(resp)
    
    oauth_authorized(provider='google', token=resp['access_token'])
    
    # Update service with user id and name
    info = google.get(endpoints['userinfo'], headers={'Authorization': 'OAuth ' + resp['access_token']})
    current_app.logger.debug(json.dumps(info.data))
    
    current_user.service('google').screen_name = info.data['email']
    db.session.commit()
    
    return redirect(url_for('account.profile'))

