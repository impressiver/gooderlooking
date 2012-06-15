# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from models import Photo

mod = Blueprint('timeline', __name__, template_folder='templates')

@mod.route("/<username>")
def post_view(username):
    photos = Photo.query.filter_by(username=username)
    return render_template('timeline.html', username=username, photos=photos)