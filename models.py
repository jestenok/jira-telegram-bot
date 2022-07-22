from sqlalchemy import Column, Integer, String, DateTime, Boolean, sql
from settings import Base, db_session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    first_name = Column(String(256))
    last_name = Column(String(256))
    language_code = Column(String(8))
    deep_link = Column(String(64))

    jira_username = Column(String(32))

    is_blocked_bot = Column(Boolean)
    is_banned = Column(Boolean)

    is_admin = Column(Boolean)
    is_moderator = Column(Boolean)

    is_bot = Column(Boolean)

    created_at = Column(DateTime, server_default=sql.func.now())
    updated_at = Column(DateTime, server_default=sql.func.now())

    waiting_for_input = Column(Boolean)
    waiting_for_announcement = Column(Boolean)

    photo_id = Column(String(255))

    def __init__(self, **kwargs: object) -> None:
        self.__dict__.update(kwargs)
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return "".format(self.username)

    def edit(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db_session.add(self)
        db_session.commit()

    @classmethod
    def get_user_from_update(cls, update):
        u = db_session.query(User).get(update.effective_user.id)
        if not u:
            u = User(**update.effective_user.to_dict())

        return u
