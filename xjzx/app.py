from flask import Flask
from user import user_blueprint
from news import news_blueprint
from admin import admin_blueprint


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(admin_blueprint)
    return app



