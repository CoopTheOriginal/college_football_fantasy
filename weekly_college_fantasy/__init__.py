from flask import Flask, render_template

from . import models
from .extensions import db, migrate, config
from .views import weekly_college_fantasy


SQLALCHEMY_DATABASE_URI = "postgresql://localhost/college_football_fantasy"
DEBUG = True
SECRET_KEY = 'development-key'


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.register_blueprint(weekly_college_fantasy)

    config.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
