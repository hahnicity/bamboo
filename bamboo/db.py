"""
bamboo.db
~~~~~~~~~
"""
from flask.ext.sqlalchemy import SQLAlchemy


def make_db(app):
    """
    Return our database engine
    """
    return SQLAlchemy(app)
