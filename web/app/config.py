from os import environ, path
from dotenv import load_dotenv


BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    FLASK_APP = environ.get('FLASK_APP')

    SESSION_PERMANENT = environ.get('SESSION_PERMANENT')
    SESSION_TYPE = environ.get('SESSION_TYPE')

    CACHE_TYPE = environ.get('CACHE_TYPE')
    CACHE_DEFAULT_TIMEOUT = int(environ.get('CACHE_DEFAULT_TIMEOUT'))


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    ODOO_SERVER_DOMAIN = environ.get('ODOO_SERVER_DOMAIN')


class ProductionConfig(Config):
    DEBUG = False
