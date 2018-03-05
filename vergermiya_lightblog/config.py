"""
Vergermiya lightblog - config.py
"""


class Config(object):
    """Base config class."""
    SECRET_KEY = "f35dcc27d30e8b46d34231c91bbeb689"


class ProdConfig(Config):
    """Production config class."""
    pass


class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    # MySQL connection
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://lightblog:lightblog+1ss@127.0.0.1:3306/vergermiya_lightblog"



