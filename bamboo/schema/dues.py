"""
bamboo.schema.dues
~~~~~~~~~~~~~~~~~~~~~~
"""
from itertools import groupby

from sqlalchemy import Column, Float, Integer, String

from bamboo.schema import Base


class Dues(Base):
    __tablename__ = "dues"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)  # XXX Add FK
    customer_owed = Column(Integer)
    amount = Column(Float)
    note = Column(String)

    def __init__(self, session, customer_id, customer_owed, amount, note):
        self.id = self.get_number_of_dues(session) + 1
        self.customer_id = customer_id
        self.customer_owed = customer_owed
        self.amount = amount
        self.note = note

    @classmethod
    def get_number_of_dues(cls, session):
        """
        Get the number of entries in this table
        """
        return session.query(cls).count()

    @classmethod
    def get_dues_by_customer_id(cls, session, id):
        """
        Get all the dues owed to/by a customer
        """
        return session.query(cls).filter(cls.customer_id==id).all()

    @classmethod
    def get_total_dues_per_friend(cls, session, id):
        """
        Get the total amount each friend owes our customer
        """
        def sum_dues(dues):
            sum = 0
            for due in dues:
                sum += due.amount
            return sum

        all_dues = cls.get_dues_by_customer_id(session, id)
        sorted_dues = sorted(all_dues, key=lambda due: due.customer_owed)
        grouped_dues = groupby(sorted_dues, key=lambda due: due.customer_owed)

        return {
            customer_id: sum_dues(dues)
            for customer_id, dues in grouped_dues
        }
