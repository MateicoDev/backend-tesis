from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils import DBSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session
from flask_cors import CORS

db = SQLAlchemy()


def get_scoped_session(uri):
    init_engine(uri)
    return scoped_session(lambda: create_session(bind=engine))


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine


def create_app():
    application = Flask(__name__)
    CORS(application)
    application.config.from_object(DBSettings)
    application.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
    application.config['CORS_SUPPORT_CREDENTIALS'] = True
    application.url_map.strict_slashes = False
    init_engine(application.config['SQLALCHEMY_DATABASE_URI'])
    global db
    db = SQLAlchemy()
    db.init_app(application)
    return application
