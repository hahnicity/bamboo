"""
bamboo.schema.customer
~~~~~~~~~~~~~~~~~~~~~~
"""
from sqlalchemy import Column, Integer, String

from bamboo.schema import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    facebook_id = Column(Integer)
    name = Column(String)

    def __init__(self, session, name, facebook_id):
        self.id = self.get_number_users(session) + 1
        self.facebook_id = facebook_id
        self.name = name

    @classmethod
    def get_user_id_by_facebook_id(cls, session, facebook_id):
        """
        Get a user id by their facebook id
        """
        return session.query(cls).filter(cls.facebook_id==facebook_id).one().id

    @classmethod
    def get_number_users(cls, session):
        """
        Get the number of rows in the customer table
        """
        return session.query(cls).count()
