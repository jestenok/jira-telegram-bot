from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine.url import URL

import os
from pathlib import Path

from telegram import Bot


with open('.env', 'r') as fh:
    vars_dict = {}
    for line in fh:
        if line.startswith('#') or line == '\n':
            continue
        key, val = line.replace('\n', '').split('=', maxsplit=1)
        vars_dict[key] = val.strip()

os.environ.update(vars_dict)
# dotenv_path = Path(__file__).parent.joinpath('.env')
# load_dotenv(dotenv_path)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(TOKEN)

JIRA_HOST = os.environ.get('JIRA_HOST')
JIRA_DOMAINNAME = os.environ.get("JIRA_DOMAINNAME")
JIRA_AUTH_LINK = f'{JIRA_DOMAINNAME}/secure/ViewProfile.jspa?' \
                 f'selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens'

DATABASE = {
    'drivername': 'postgresql',
    'host': os.environ.get('DB_HOST'),
    'port': '5432',
    'database': 'server',
    'username': os.environ.get('DB_USERNAME'),
    'password': os.environ.get('PASSWORD')
}

engine = create_engine(URL.create(**DATABASE),
                       connect_args={'options': '-csearch_path={}'.format('telegram')})

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
