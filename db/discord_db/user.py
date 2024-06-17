from base import Base

from sqlalchemy import Column, String, ARRAY

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    roles = Column(ARRAY(String), nullable=False)

    def __repr__(self):
        return f'username: {self.username} roles: {self.roles}'
