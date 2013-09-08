"""
bamboo.connection
~~~~~~~~~~~~~~~~~
"""
from contextlib import contextmanager

from flask.ext.sqlalchemy import SQLAlchemy


def initialize_db():
    """
    Initialize our database
    """
    from bamboo.globals import db
    from bamboo.schema import Customer, Dues
    db.create_all()


def make_db(app):
    """
    Return our database engine
    """
    return SQLAlchemy(app)


@contextmanager
def execute_session():
    """
    Execute some kind of action with a session object
    """
    from bamboo.globals import db
    try:
        yield db.session
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
