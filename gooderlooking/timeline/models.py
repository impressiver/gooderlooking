# -*- coding:utf-8 -*-
from database import db
from datetime import datetime

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    pub_date = db.Column(db.DateTime)
    title = db.Column(db.String(255))

    def __init__(self, title, pub_date=None):
        self.title = title
        self.pub_date = (pub_date or datetime.utcnow())

    def __repr__(self):
        return self.title
