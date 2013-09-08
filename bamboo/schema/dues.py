"""
bamboo.schema.dues
~~~~~~~~~~~~~~~~~~~~~~
"""
from sqlalchemy import Column, Integer, String

from bamboo.schema import Base


class Dues(Base):
    __tablename__ = "dues"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)  # XXX Add FK
    customer_owed = Column(Integer)
    amount = Column(Integer)
    note = Column(String)

    def __init__(self, session, customer_id, customer_owed, amount, note):
        self.id = self.get_number_of_dues(session) + 1
        self.customer_id = customer_id
        self.customer_owed = customer_owed
        self.amount = amount
        self.note = note

    def get_number_of_dues(self, session):
        """
        Get the number of entries in this table
        """
        return session.query(self).count()

    @classmethod
    def get_dues_by_customer_id(cls, session, id):
        """
        Get all the dues owed to/by a customer
        """
        return session.query(cls).filter(cls.customer_id==id)
