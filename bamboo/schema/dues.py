"""
bamboo.schema.dues
~~~~~~~~~~~~~~~~~~~~~~
"""
from itertools import groupby

from bamboo.globals import db
from bamboo.schema.base import get_last_id


class Dues(db.Model):
    __tablename__ = "dues"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # XXX Add FK
    friend_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    note = db.Column(db.String)

    def __init__(self, session, user_id, friend_id, amount, note):
        self.id = self.get_last_due_id(session) + 1
        self.user_id = user_id
        self.friend_id = friend_id
        self.amount = amount
        self.note = note

    @classmethod
    def delete_dues_by_friend(cls, session, user_id, friend_id):
        """
        Remove all dues associated with a friend
        """
        session.query(cls).filter(
            cls.user_id==user_id,
            cls.friend_id==friend_id
        ).delete()

    @classmethod
    def get_last_due_id(cls, session):
        """
        Get the number of entries in this table
        """
        return get_last_id(cls, session)

    @classmethod
    def get_all_dues_for_customer(cls, session, user_id):
        """
        Get all the dues owed to/by a user
        """
        return session.query(cls).filter(cls.user_id==user_id).all()

    @classmethod
    def get_dues_by_friend(cls, session, user_id, friend_id):
        return session.query(cls).filter(
            cls.user_id==user_id, cls.friend_id==friend_id
        ).all()

    @classmethod
    def get_dues_for_customer_by_friend(cls, session, user_id, friend_id):
        """
        Get all dues owed to/by a user for a specific friend
        """
        dues = cls.get_dues_by_friend(session, user_id, friend_id)
        return [{
            "due_id": due.user_id,
            "amount": due.amount,
            "note": due.note
        } for due in dues]

    @classmethod
    def get_sum_dues_for_customer_by_friend(cls, session, user_id, friend_id):
        """
        Get the sum of dues owed to/by a user for a specifi
        """
        dues = cls.get_dues_by_friend(session, user_id, friend_id)
        return cls.sum_dues(dues)

    @classmethod
    def get_total_dues_per_friend(cls, session, user_id):
        """
        Get the total amount each friend owes our user
        """
        all_dues = cls.get_all_dues_for_customer(session, user_id)
        sorted_dues = sorted(all_dues, key=lambda due: due.friend_id)
        grouped_dues = groupby(sorted_dues, key=lambda due: due.friend_id)

        return {
            user_id: cls.sum_dues(dues) for user_id, dues in grouped_dues
        }

    @classmethod
    def sum_dues(cls, dues):
        """
        Get a sum of all dues in a list
        """
        sum = 0
        for due in dues:
            sum += due.amount
        return sum
