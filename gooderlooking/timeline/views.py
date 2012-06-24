# -*- coding:utf-8 -*-
from flask import Blueprint, current_app, render_template, request, session, flash, redirect, url_for
from flask.ext.security import (current_user, login_required)
from flaskext.uploads import IMAGES, UploadNotAllowed
from flaskext.wtf import (Form, TextField, FileField, QuerySelectField, file_allowed, file_required)
from wtforms.ext.sqlalchemy.orm import model_form
from database import db
from account.models import User
from models import Album, Photo
from uploader import photos as uploaded_photos

mod = Blueprint('timeline', __name__, template_folder='templates')

@mod.route("/<username>")
def main(username):
    photos = Photo.query.filter(User.username == username)
    return render_template('timeline.html', username=username, photos=photos)
    
@mod.route("/photo/<int:photo_id>")
def photo(photo_id):
    photo = Photo.query.filter_by(id=photo_id).one()
    
    return render_template('photo.html', username=photo.user.username, photo=photo)
    
@mod.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = PhotoForm()
    #form = model_form(Photo, converter=RelationalModelConverter(db.session))
    #form = model_form(Photo)
    
    # Multiple files
    #request.files.getlist('file')
    
    if request.method == 'POST':
        if not (form.photo.data):
            flash("You must select an image file to upload")
        else:            
            album = form.album.data
            photo = form.photo.data
            title = form.title.data
            caption = form.caption.data
                
            try:
                filename = uploaded_photos.save(photo, folder=str(current_user.id), name=photo.filename)
            except UploadNotAllowed:
                flash("The upload was not allowed")
            else:
                # album = Album(user_id=current_user.id, title=form.album_title.data)
                # db.session.add(album)
                # db.session.commit()
                
                post = Photo(user_id=current_user.id, album_id=album, title=title, caption=caption, url=filename)
                db.session.add(post)
                db.session.commit()
                
                flash("Post successful")
                return redirect(url_for('.main', username=current_user.username))
                
    return render_template('upload.html', form=form)
    
def _user_albums_query_factory():
    return Album.query.filter_by(user_id=current_user.id)
    
class PhotoForm(Form):
    """The photo upload form"""
    
    album = QuerySelectField(get_label='title', query_factory=_user_albums_query_factory, allow_blank=True, blank_text="Unsorted")
    #album_title = TextField("Album Title")
    
    photo = FileField("New Photo",
       validators=[file_required(),
                   file_allowed(IMAGES, "Only images are allowed")])
    title = TextField("Title")
    caption = TextField("Caption")

    def to_dict(self):
        return dict(album=self.album.data, photo=self.photo.data, title=self.title.data, caption=self.caption.data)