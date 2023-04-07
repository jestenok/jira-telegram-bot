from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine.url import URL

import logging

import os
import sys


# Bot
TG_HOST = os.getenv('TG_HOST')
TG_TOKEN = os.getenv('TG_TOKEN')
TG_USE_WEBHOOK = os.getenv('TG_USE_WEBHOOK', 'false') == 'true'


# Jira
JIRA_HOST = os.getenv("JIRA_HOST")
JIRA_PUBLIC_HOST = os.getenv("JIRA_PUBLIC_HOST")
JIRA_AUTH_LINK = f'{JIRA_PUBLIC_HOST}/secure/ViewProfile.jspa?' \
                 f'selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens'


# Logging
LOG_DIR = os.getenv('LOG_DIR')
if LOG_DIR is None:
    LOG_DIR = '/var/log/jira-telegram-bot'
os.mkdir(LOG_DIR) if not os.path.exists(LOG_DIR) else None

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-0.12s] [%(levelname)-0.5s] %(message)s")

fileHandler = logging.FileHandler("{0}/{1}.log".format(LOG_DIR, "bot"))
fileHandler.setFormatter(logFormatter)

rootLogger = logging.getLogger()
rootLogger.addHandler(fileHandler)
rootLogger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

# Database
DATABASE = {
    'drivername': 'postgresql',
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD')
}


engine = create_engine(URL.create(**DATABASE))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)

