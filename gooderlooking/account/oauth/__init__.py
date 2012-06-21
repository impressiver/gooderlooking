from .core import *

def register(app):
    from account.oauth import (views, facebook, twitter, google, foursquare)
    
    app.register_blueprint(views.mod)
    
    app.register_blueprint(facebook.mod)
    app.register_blueprint(twitter.mod)
    app.register_blueprint(google.mod)
    app.register_blueprint(foursquare.mod)