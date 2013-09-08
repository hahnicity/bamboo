"""
bamboo.schema.customer
~~~~~~~~~~~~~~~~~~~~~~
"""
from bamboo.globals import db


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    facebook_id = db.Column(db.Integer)
    name = db.Column(db.String)

    def __init__(self, session, name, facebook_id):
        self.id = self.get_last_user_id(session) + 1
        self.facebook_id = facebook_id
        self.name = name

    @classmethod
    def get_name_by_id(cls, session, id):
        return session.query(cls).filter(cls.id==id).one().name

    @classmethod
    def get_user_id_by_facebook_id(cls, session, facebook_id):
        """
        Get a user id by their facebook id
        """
        return session.query(cls).filter(cls.facebook_id==facebook_id).one().id

    @classmethod
    def get_last_user_id(cls, session):
        """
        Get the number of rows in the customer table
        """
        if session.query(cls).count() == 0:
            return 0
        else:
            return session.query(cls).order_by("-id").first().id
