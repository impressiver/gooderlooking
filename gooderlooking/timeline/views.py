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

# http://pydoc.net/Flask-Admin/0.2.2/flask_admin
import json
import inspect
import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound
from wtforms import widgets, validators
from wtforms import fields as wtf_fields
from wtforms.ext.sqlalchemy.orm import model_form, converts, ModelConverter
from wtforms.ext.sqlalchemy import fields as sa_fields

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
    
def _user_albums():
    return Album.query.filter_by(user_id=current_user.id)
    
class PhotoForm(Form):
    """The photo upload form"""
    
    album = QuerySelectField(get_label='title', query_factory=_user_albums, allow_blank=True, blank_text="Unsorted")
    #album_title = TextField("Album Title")
    
    photo = FileField("New Photo",
       validators=[file_required(),
                   file_allowed(IMAGES, "Only images are allowed")])
    title = TextField("Title")
    caption = TextField("Caption")

    def to_dict(self):
        return dict(photo=self.photo.data, title=self.title.data, caption=self.caption.data)
        
        
def _query_factory_for(model_class, db_session):
    """
    Return a query factory for a given model_class. This gives us an
    all-purpose way of generating query factories for
    QuerySelectFields.
    """
    def query_factory():
        return sorted(db_session.query(model_class).all(), key=repr)
 
    return query_factory
    
class RelationalModelConverter(ModelConverter):
    """
    Subclass of the wtforms sqlalchemy Model Converter that handles
    relationship properties and uses custom widgets for date and
    datetime objects.
    """
    def __init__(self, db_session, *args, **kwargs):
        self.db_session = db_session
        super(RelationalModelConverter, self).__init__(*args, **kwargs)
 
    def convert(self, model, mapper, prop, field_args):
        if not isinstance(prop, sa.orm.properties.ColumnProperty) and \
               not isinstance(prop, sa.orm.properties.RelationshipProperty):
            # XXX We don't support anything but ColumnProperty and
            # RelationshipProperty at the moment.
            return
 
        if isinstance(prop, sa.orm.properties.ColumnProperty):
            if len(prop.columns) != 1:
                raise TypeError('Do not know how to convert multiple-'
                                'column properties currently')
 
            column = prop.columns[0]
            kwargs = {
                'validators': [],
                'filters': [],
                'default': column.default,
            }
            if field_args:
                kwargs.update(field_args)
            if column.nullable:
                kwargs['validators'].append(validators.Optional())
            if self.use_mro:
                types = inspect.getmro(type(column.type))
            else:
                types = [type(column.type)]
 
            converter = None
            for col_type in types:
                type_string = '%s.%s' % (col_type.__module__,
                                         col_type.__name__)
                if type_string.startswith('sqlalchemy'):
                    type_string = type_string[11:]
                if type_string in self.converters:
                    converter = self.converters[type_string]
                    break
            else:
                for col_type in types:
                    if col_type.__name__ in self.converters:
                        converter = self.converters[col_type.__name__]
                        break
                else:
                    return
            return converter(model=model, mapper=mapper, prop=prop,
                             column=column, field_args=kwargs)
 
        if isinstance(prop, sa.orm.properties.RelationshipProperty):
            if prop.direction == sa.orm.interfaces.MANYTOONE and \
                   len(prop.local_remote_pairs) != 1:
                raise TypeError('Do not know how to convert multiple'
                                '-column properties currently')
            elif prop.direction == sa.orm.interfaces.MANYTOMANY and \
                     len(prop.local_remote_pairs) != 2:
                raise TypeError('Do not know how to convert multiple'
                                '-column properties currently')
 
            local_column = prop.local_remote_pairs[0][0]
            foreign_model = prop.mapper.class_
 
            if prop.direction == sa.orm.properties.MANYTOONE:
                return sa_fields.QuerySelectField(
                    foreign_model.__name__,
                    query_factory=_query_factory_for(foreign_model,
                                                     self.db_session),
                    allow_blank=local_column.nullable)
            if prop.direction == sa.orm.properties.MANYTOMANY:
                return sa_fields.QuerySelectMultipleField(
                    foreign_model.__name__,
                    query_factory=_query_factory_for(foreign_model,
                                                     self.db_session),
                    allow_blank=local_column.nullable)