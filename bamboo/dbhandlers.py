"""
bamboo.dbhandlers
~~~~~~~~~~~~~~~~~
"""
from sqlalchemy.orm.exc import NoResultFound

from bamboo.connection import execute_session
from bamboo.schema import Customer, Dues
from bamboo.oauth import get_user_id, get_user_name


def handle_login(user):
    """
    Handle all aspects of login, return the user id
    """
    with execute_session() as session:
        try:
            return Customer.get_user_id_by_facebook_id(
                session, get_user_id(user)
            )
        except NoResultFound:
            session.add(Customer(
                session, get_user_name(user), get_user_id(user)
            ))
            # XXX HACK
            session.commit()
            return Customer.get_user_id_by_facebook_id(
                session, get_user_id(user)
            )


def handle_new_due(form):
    """
    Handle the creation of a new due
    """
    with execute_session() as session:
        session.add(Dues(
            session,
            form["id"],
            form["customer_owed"],
            form["amount"],
            form["note"]
        ))


def handle_view_dues(id):
    """
    Handle viewing dues owed to/by other customers
    """
    with execute_session() as session:
        dues = Dues.get_total_dues_per_friend(session, id)
        return {
            Customer.get_name_by_id(session, id): amount
            for id, amount in dues.iteritems()
        }
