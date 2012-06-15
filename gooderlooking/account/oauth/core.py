# -*- coding: utf-8 -*-
from flask import (Blueprint, current_app, request, g, session, redirect, flash, render_template, url_for)
from flask.ext.security import (current_user, login_required)
from flask.ext.security.exceptions import UserNotFoundError
from flask.ext.oauth import OAuth
from sqlalchemy.orm.exc import NoResultFound
from database import db
from account.models import User, Service

oauth = OAuth()

def oauth_authorized(**kwargs):
    current_app.logger.debug(kwargs)
    
    if id and current_user.is_authenticated():
        # try:
        #     user = User.query.filter(User.services.any(id=id)).one()
        #     current_app.logger.debug("user is already authenticated, wtf")
        # except NoResultFound:
        current_user.services[kwargs['provider']] = Service(**kwargs)
        db.session.commit();
    else:
        current_app.logger.debug("Current user isn't authenticated, can't authorize %s (id: %s)", service, id)