from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column

Base = declarative_base()


class GitHubUserORM(Base):
    __tablename__ = "githubuser"

    user_id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String(39), unique=True)
    email = mapped_column(String(254), unique=True)

    repositories = relationship("RepositoryORM", back_populates="user")


class RepositoryORM(Base):
    __tablename__ = "repository"

    repoid = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(255))
    forks = mapped_column(Integer)
    stars = mapped_column(Integer)
    commits = mapped_column(Integer)
    pullrequests = mapped_column(Integer)
    issues = mapped_column(Integer)
    comments = mapped_column(Integer)
    watchers = mapped_column(Integer)
    views = mapped_column(Integer)
    activeusers = mapped_column(Integer)
    userid = mapped_column(Integer, ForeignKey("githubuser.user_id"))
    fetched_at = mapped_column(DateTime, index=True)

    user = relationship("GitHubUserORM", back_populates="repositories")
