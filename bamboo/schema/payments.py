"""
bamboo.schema.payments
~~~~~~~~~~~~~~~~~~~~~~
"""
from bamboo.globals import db


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
        if session.query(cls).count() == 0:
            return 0
        else:
            return session.query(cls).order_by("-id").first().id
