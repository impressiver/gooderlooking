# -*- coding:utf-8 -*-
from flask import g, Blueprint, redirect, session, current_app, url_for
from flask.ext.security import current_user
from account.oauth import oauth, oauth_authorized

mod = Blueprint('twitter', __name__, url_prefix='/oauth/twitter')

twitter = oauth.remote_app('twitter',
    base_url = 'https://api.twitter.com/1/',
    request_token_url = 'https://api.twitter.com/oauth/request_token',
    access_token_url = 'https://api.twitter.com/oauth/access_token',
    authorize_url = 'https://api.twitter.com/oauth/authorize',
    consumer_key = 'tEX6iFRU3XQCcf2Mxp0Q',
    consumer_secret = 'U83LOxIg0AiZLO3c3AtUlpGOf0TREj0WSecW6pRb7k'
)

@twitter.tokengetter
def twitter_token():
    if current_user.is_authenticated():
        service = current_user.service('twitter')
        if service:
            return service.token, service.secret


@mod.route('/signin')
def twitter_signin():
    return twitter.authorize(callback='http://gooderlooking.com/oauth/twitter/authorized')


@mod.route('/authorized')
@twitter.authorized_handler
def twitter_authorized(resp):    
    oauth_authorized(provider='twitter', service_user_id=resp['user_id'], screen_name=resp['screen_name'], token=resp['oauth_token'], secret=resp['oauth_token_secret'])
    return redirect(url_for('account.profile'))