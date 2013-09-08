"""
bamboo.schema.base
~~~~~~~~~~~~~~~~~~

Common functions that can be implemented across tables
"""


def get_last_id(obj, session):
    """
    Get the last id in a table
    """
    try:
        return session.query(obj).order_by("-id").first().id
    except AttributeError:  # This will be thrown for no entries
        return 0
