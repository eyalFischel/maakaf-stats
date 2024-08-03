# import pytest
# from datetime import datetime
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from discord_db.modules import Base, Channel, Message, User
# from your_module import insert_user, insert_channel, insert_message, update_channel

# # Setup in-memory SQLite database for testing
# DATABASE_URL = "sqlite:///:memory:"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def db_session():
#     # Create tables
#     Base.metadata.create_all(bind=engine)
#     session = SessionLocal()
#     yield session
#     session.close()
#     Base.metadata.drop_all(bind=engine)

# def test_insert_user(db_session):
#     insert_user(db_session, "testuser", datetime.now())
#     user = db_session.query(User).filter_by(username="testuser").first()
#     assert user is not None
#     assert user.username == "testuser"

# def test_insert_channel(db_session):
#     insert_channel(db_session, "channel1", "general")
#     channel = db_session.query(Channel).filter_by(channel_id="channel1").first()
#     assert channel is not None
#     assert channel.name == "general"

# def test_insert_message(db_session):
#     insert_user(db_session, "testuser", datetime.now())
#     insert_channel(db_session, "channel1", "general")
#     insert_message(db_session, "message1", "channel1", "testuser", datetime.now())
#     message = db_session.query(Message).filter_by(message_id="message1").first()
#     assert message is not None
#     assert message.username == "testuser"

# def test_update_channel(db_session):
#     insert_channel(db_session, "channel1", "general")
#     update_channel(db_session, "channel1", "random")
#     channel = db_session.query(Channel).filter_by(channel_id="channel1").first()
#     assert channel is not None
#     assert channel.name == "random"


#generated example