# -*- coding:utf-8 -*-
from flask import current_app
from flask.ext.security import (UserMixin, RoleMixin)
from sqlalchemy.orm.collections import attribute_mapped_collection
from database import db
from datetime import datetime


role_user = db.Table('role_user',
    db.Column('user_id', db.Integer(), db.ForeignKey('role.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('user.id')))

class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=db.func.now())

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model, TimestampMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    openid = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(200))
    nickname = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=role_user,
        backref=db.backref('users', lazy='dynamic'))
    services = db.relationship("Service", backref="user", collection_class=attribute_mapped_collection('provider'), cascade="all, delete-orphan")

    def service(self, name):
        if name in self.services:
            return self.services[name]
        return None
        
        
class Service(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.Enum("google", "facebook", "twitter", "foursquare"))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    service_user_id = db.Column(db.Integer())
    screen_name = db.Column(db.String(120))
    token = db.Column(db.Text())
    secret = db.Column(db.Text())
    expires = db.Column(db.DateTime())
    
    def __init__(self, **kwargs):
        self.provider = kwargs['provider']
        self.token = kwargs['token']
        if 'service_user_id' in kwargs: self.service_user_id = kwargs['service_user_id']
        if 'screen_name' in kwargs: self.screen_name = kwargs['screen_name']
        if 'secret' in kwargs: self.secret = kwargs['secret']
        if 'expires' in kwargs: self.expires = kwargs['expires']