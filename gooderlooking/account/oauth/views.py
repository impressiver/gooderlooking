# -*- coding:utf-8 -*-
from flask import (Blueprint, current_app, request, g, session, redirect, flash, render_template, url_for)
from flask.ext.security import (current_user, login_required)
from database import db

mod = Blueprint('oauth', __name__, url_prefix='/oauth')

def init_blueprint(state):
    from account.oauth import twitter, facebook
    
    app = state.app
    
    app.register_blueprint(twitter.mod)
    app.register_blueprint(facebook.mod)


@mod.route('/unlink/<target>')
def unlink(target):
    current_app.logger.debug("unlink: %s", target)
    
    service = current_user.service(target)
    if service:
        current_user.services.remove(service)
        db.session.commit()
    
    
    return redirect(url_for('account.profile'))
    
