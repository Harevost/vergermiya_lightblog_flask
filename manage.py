"""
Vergermiya lightblog - script.py
"""

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from vergermiya_lightblog.models import db, User, Post, Comment, Tag
from vergermiya_lightblog import app

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("server", Server(host="0.0.0.0", port=80))
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    """
    create a python CLI
    :return: Default import project
    """
    return dict(app=app, db=db,
                User=User, Post=Post,
                Comment=Comment, Tag=Tag)


if __name__ == '__main__':
    manager.run()

