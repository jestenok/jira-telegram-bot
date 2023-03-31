from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine.url import URL
import logging

import os

from telegram import Bot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(TOKEN)

JIRA_HOST = os.environ.get('JIRA_HOST')

JIRA_PUBLIC_DOMAINNAME = os.environ.get("JIRA_PUBLIC_DOMAINNAME")
JIRA_AUTH_LINK = f'{JIRA_PUBLIC_DOMAINNAME}/secure/ViewProfile.jspa?' \
                 f'selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens'

DATABASE = {
    'drivername': 'postgresql',
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'database': os.environ.get('DB_NAME'),
    'username': os.environ.get('DB_USERNAME'),
    'password': os.environ.get('DB_PASSWORD')
}

engine = create_engine(URL.create(**DATABASE))

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


def init_db():
    Base.metadata.create_all(bind=engine)
