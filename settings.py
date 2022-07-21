from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine.url import URL

import os
from pathlib import Path

from telegram import Bot

from dotenv import load_dotenv


dotenv_path = Path(__file__).parent.joinpath('.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(TOKEN)

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
    import models
    Base.metadata.create_all(bind=engine)
