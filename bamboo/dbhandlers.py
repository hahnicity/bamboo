"""
bamboo.dbhandlers
~~~~~~~~~~~~~~~~~
"""
from sqlalchemy.orm.exc import NoResultFound

from bamboo.connection import execute_session
from bamboo.schema import Customer, Dues, Payments
from bamboo.thirdparty import get_facebook_user_id, get_facebook_name


def handle_login(user):
    """
    Handle all aspects of login, return the user id
    """
    with execute_session() as session:
        try:
            return Customer.get_user_id_by_facebook_id(
                session, get_facebook_user_id(user)
            )
        except NoResultFound:
            session.add(Customer(
                session, get_facebook_name(user), get_facebook_user_id(user)
            ))
            # XXX HACK
            session.commit()
            return Customer.get_user_id_by_facebook_id(
                session, get_facebook_user_id(user)
            )


def handle_new_due(form):
    """
    Handle the creation of a new due
    """
    with execute_session() as session:
        session.add(Dues(
            session,
            form["id"],  # XXX Customer ID
            form["friend_id"],  # XXX Friend id
            form["amount"],
            form["note"]
        ))


def handle_pay_in_full(form):
    """
    Handle a user paying their debts in full
    """
    with execute_session() as session:
        amount = Dues.get_sum_dues_for_customer_by_friend(
            session, form["id"], form["friend_id"]
        )
        # XXX Handle VenMo
        session.add(Payments(session, form["id"], form["friend_id"], amount))
        Dues.delete_dues_by_friend(session, form["id"], form["friend_id"])


def handle_view_dues(id):
    """
    Handle viewing dues owed to/by other customers
    """
    with execute_session() as session:
        dues = Dues.get_total_dues_per_friend(session, id)
        return [{
            "name": Customer.get_name_by_id(session, id),
            "amount": amount,
            "friend_id": id
        } for id, amount in dues.iteritems()]


def handle_view_dues_by_friend(id, friend_id):
    """
    Handle viewing specific dues for a single friend
    """
    with execute_session() as session:
        return Dues.get_dues_for_customer_by_friend(session, id, friend_id)
