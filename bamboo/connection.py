"""
bamboo.connection
~~~~~~~~~~~~~~~~~
"""
from contextlib import contextmanager

from bamboo.globals import db


def add_and_commit(session, item):
    """
    Add an item to the DB and then commit it
    """
    session.add(item)
    session.commit()


@contextmanager
def execute_session():
    """
    Execute some kind of action with a session object
    """
    try:
        yield db.session
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()


def make_schema():
    """
    Initialize our database
    """
    db.create_all()
