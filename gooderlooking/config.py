# -*- config:utf-8 -*-
from datetime import timedelta

project_name = "gooderlooking"

class Config(object):
    # APP
    BUILD = 123
    
    # FLASK
    DEBUG = True
    TESTING = False
    USE_X_SENDFILE = False
    
    # LOGGING
    LOGGER_NAME = "%s_log" % project_name
    SENTRY_DSN = 'https://a5a5e906a1e04d8b80ef0709fb18da50:bbd0a1fb764b47a99d0e83615ceb7057@app.getsentry.com/1134'
    SENTRY_INCLUDE_PATHS = [project_name]

    # DATABASE
    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/%s_dev" % project_name
    SQLALCHEMY_ECHO = True
    
    # SESSIONS
    CSRF_ENABLED = True
    SECRET_KEY = '\xd2S\xe2KJY\xa4J\xaf\x0b\xe3\x9a\x96Q\xa0\xd6\xb7\xa1\xed\xa9\xacp\xe0\xcc'  # import os; os.urandom(24)
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # AUTHENTICATION & AUTHORIZATION
    SECURITY_AUTH_PROVIDER = 'account.openid::OpenIDAuthenticationProvider'
    SECURITY_LOGIN_VIEW = '/openid/login'
    SECURITY_POST_LOGIN_VIEW = '/profile'
    OPENID_FS_STORE_PATH = '/tmp/flask-openid'
    COMMON_PROVIDERS = {
        'google':       'https://www.google.com/accounts/o8/id',
        'yahoo':        'https://yahoo.com/',
        'aol':          'http://aol.com/',
        'steam':        'https://steamcommunity.com/openid/'
    }

    # EMAIL
    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    DEFAULT_MAIL_SENDER = "example@%s.com" % project_name

    # ex: BLUEPRINTS = ['blog.views.app']  # where app is a Blueprint instance
    # ex: BLUEPRINTS = [('blog.views.app', {'url_prefix': '/myblog'})]  # where app is a Blueprint instance
    BLUEPRINTS = [
        'account.views.mod',
        ('timeline.views.mod', {'url_prefix': '/timeline'})
    ]
    
    # QUEUE
    CELERY_CONFIG_MODULE = "gooderlooking.config"
    CELERY_RESULT_BACKEND = "redis"
    CELERY_REDIS_HOST = "localhost"
    CELERY_REDIS_PORT = 6379
    CELERY_REDIS_DB = 0

    BROKER_URL = 'redis://localhost:6379/0'
    
    # UPLOADS
    UPLOADS_DEFAULT_DEST = 'static/uploads'
    UPLOADS_DEFAULT_URL = '/static/uploads'
    
    # ASSETS
    ASSETS_DEBUG = False
    ASSETS_VERSIONS = 'build'
    ASSETS_SCRIPTS = {
        'boot': [
            'scripts/jquery-1.7.2.js',
            'lib/jquery-ui-1.8.21/development-bundle/ui/jquery.ui.core.js',
            'scripts/spin.js',
            'scripts/app.js'
        ],
        'timelines': [
            'scripts/timelines.js'
        ]
    }
    ASSETS_STYLES = {
        'boot': [
            'styles/reset.css',
            'styles/site.css',
            'styles/theme.responsive.css'
        ],
        'timelines': [
            'styles/timelines.css'
        ]
    }

class Prod(Config):
    DEBUG = False
    ASSETS_DEBUG = False
    
    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/%s" % project_name
    SQLALCHEMY_ECHO = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
        

class Dev(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class Testing(Config):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/%s_test" % project_name
    SQLALCHEMY_ECHO = False


class PyCharm(Dev):
    DEBUG = False
    THREADED = True
    SQLALCHEMY_ECHO = True