"""
Vergermiya lightblog - script.py
"""
import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from vergermiya_lightblog import create_app
from vergermiya_lightblog import models


env = os.environ.get("BLOG_ENV", "dev")
app = create_app("vergermiya_lightblog.config.%sConfig" % env.capitalize())
manager = Manager(app)
migrate = Migrate(app, models.db)

manager.add_command("server", Server(host="0.0.0.0", port=80))
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    """
    create a python CLI
    :return: Default import project
    """
    return dict(app=app, db=models.db,
                User=models.User, Post=models.Post,
                Comment=models.Comment, Tag=models.Tag,
                Server=Server)


if __name__ == '__main__':
    manager.run()

