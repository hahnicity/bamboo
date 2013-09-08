"""
bamboo.schema.friends
~~~~~~~~~~~~~~~~~~~~~
"""
from sqlalchemy import Column, Integer

from bamboo.schema import Base


class Friends(Base):
    __tablename__ = "friends"

    customer_id = Column(Integer, primary_key=True)  # XXX Add FK
    friend_id = Column(Integer)

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.friend_id = friend_id
