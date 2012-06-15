from .core import *


def register(app):
    import views
    
    app.register_blueprint(views.mod)