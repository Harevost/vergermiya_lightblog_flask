"""
Vergermiya lightblog - __init__.py
"""

from flask import Flask, redirect, url_for
from vergermiya_lightblog.config import DevConfig
from vergermiya_lightblog.models import db
from vergermiya_lightblog.controllers import blog, account
from vergermiya_lightblog.extensions import bcrypt


def create_app(object_name):
    """
    Create the app instance by factory mode
    """

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)


    @app.route('/')
    def index():
        return redirect(url_for('blog.index'))

    app.register_blueprint(blog.blog_blueprint)
    app.register_blueprint(account.account_blueprint)

    return app
