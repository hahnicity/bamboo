"""
bamboo.schema.payments
~~~~~~~~~~~~~~~~~~~~~~
"""
from bamboo.globals import db
from bamboo.schema.base import get_last_id


class Payments(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    to_ = db.Column(db.Integer)
    from_ = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def __init__(self, session, to_, from_, amount):
        self.id = self.get_last_payment(session) + 1
        self.to_ = to_
        self.from_ = from_
        self.amount = amount

    @classmethod
    def get_last_payment(cls, session):
        """
        Get the id of the last payment made
        """
        return get_last_id(cls, session)
