from sqlalchemy import Column, Integer, String, DateTime, Boolean, sql
from app.settings import Base, db_session, JIRA_HOST
from jira import JIRA


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    first_name = Column(String(256))
    last_name = Column(String(256))
    language_code = Column(String(8))
    deep_link = Column(String(64))

    jira_username = Column(String(32))
    jira_token = Column(String(50))

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

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return self.username

    def edit(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db_session.add(self)
        db_session.commit()

    def jira_session(self, token=None):
        if token:
            jira = JIRA(JIRA_HOST, token_auth=token)
            try:
                jira_username = jira.current_user()
            except:
                return None

            self.edit(jira_username=jira_username, jira_token=token)

        return JIRA(JIRA_HOST, token_auth=self.jira_token)

    @classmethod
    def get_user_from_update(cls, update):
        u = db_session.query(User).get(update.effective_user.id)
        if not u:
            u = User(**update.effective_user.to_dict())

        return u

    @classmethod
    def get_user_by_jira_username(cls, jira_username):
        return db_session.query(User).filter(User.jira_username == jira_username).first()
