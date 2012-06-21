# -*- coding:utf-8 -*-
from database import db
from uploader import photos as uploaded_photos
from datetime import datetime


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider = db.Column(db.Enum("google", "facebook", "twitter", "foursquare"))
    service_album_id = db.Column(db.Integer())
    title = db.Column(db.String(255))
    description = db.Column(db.Text())
    pub_date = db.Column(db.DateTime)
    photos = db.relationship("Photo", backref="album")
    
    user = db.relationship("User")

    def __init__(self, user_id, provider=None, service_album_id=None, title=None, description=None, pub_date=None):
        self.user_id = user_id
        self.provider = provider
        self.service_album_id = service_album_id
        self.title = title
        self.description = description
        self.pub_date = (pub_date or datetime.utcnow())


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    album_id = db.Column(db.Integer(), db.ForeignKey('album.id'))
    url = db.Column(db.String(255))
    service_photo_id = db.Column(db.Integer())
    pub_date = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    caption = db.Column(db.Text())
    
    user = db.relationship("User")

    def __init__(self, user_id, url, album_id=None, title=None, caption=None, service_photo_id=None, pub_date=None):
        self.user_id = user_id
        self.url = url
        self.album_id = album_id
        self.service_photo_id = service_photo_id
        self.title = title
        self.caption = caption
        self.pub_date = (pub_date or datetime.utcnow())

    def __repr__(self):
        return self.title
        
    def get_url(self):
        return uploaded_photos.url(self.url)
