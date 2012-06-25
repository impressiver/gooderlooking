from flask import (Blueprint, current_app, request, g, session, redirect, flash, render_template, url_for)
from flask.ext.security import (Security, current_user, login_required)
from flask.ext.security.signals import user_registered
from flask.ext.security.exceptions import UserNotFoundError
from flask.ext.celery import Celery
from database import db
import openid


mod = Blueprint('account', __name__, template_folder='templates')


def init_blueprint(state):
    import openid, oauth
    
    app = state.app
    
    openid.register(app)
    oauth.register(app)
        
                                   
@mod.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if current_user.is_authenticated() or 'openid' not in session:
        return redirect(url_for('account.profile'))
        
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        if not username:
            flash(u'Error: you have to provide a username')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            user = current_app.security.datastore.create_user(username=username, email=email, nickname=name, password='openid', openid=session['openid'], active=True)
            user_registered.send(user, app=current_app._get_current_object())
            flash(u'Profile successfully created')
            return redirect(openid.views.oid.get_next_url())
            
    return render_template('create_profile.html', next_url=openid.views.oid.get_next_url())


@mod.route('/profile')
@login_required
def profile():
    from flask.ext.optimize import Optimize

    optimize = Optimize()
    optimize.init_app(current_app)

    optimize.smush('static/uploads/blog-splash_1.png', 'static/uploads/blog-splash_1-optim.png')
    
    return render_template('profile.html', content='Profile');


mod.record(init_blueprint)