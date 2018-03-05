"""
Vergermiya lightblog - __init__.py
"""

from flask import Flask, redirect, url_for
from vergermiya_lightblog.config import DevConfig
from vergermiya_lightblog.models import db
from vergermiya_lightblog.controllers import blog

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)


@app.route('/')
def index():
    return redirect(url_for('blog.index'))

app.register_blueprint(blog.blog_blueprint)

if __name__ == "__main__":
    app.register_blueprint(blog.blog_blueprint)
    app.run()
