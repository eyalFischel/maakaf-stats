from db.discord_db.db import Base

from sqlalchemy import String, ARRAY
from sqlalchemy.orm import mapped_column

class User(Base):
    __tablename__: str = 'users'

    username = mapped_column(String, primary_key=True)
    roles = mapped_column(ARRAY(String), nullable=False)

    def __repr__(self) -> str:
        return f'username: {self.username} roles: {self.roles}'