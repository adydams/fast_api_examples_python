from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
from sqlalchemy.orm import sessionmaker
from decouple import config

try:
    from urllib import quote  as urlquote # Python 2.X
except ImportError:
    from urllib.parse import quote as urlquote # Python 3+



#when passing the data directly
#check in .env file
DATABASE_USERNAME_Val = config('DATABASE_USERNAME')
DATABASE_HOSTNAME_Val = config('DATABASE_HOSTNAME')
DATABASE_PASSWORD_Val = config('DATABASE_PASSWORD')
DATABASE_NAME_Val = config('DATABASE_NAME')
DATABASE_PORT_Val = int(config('DATABASE_PORT'))

#when using .env
SQLALCHEMY_DATABASE_URL= f'postgresql://{DATABASE_USERNAME_Val}:%s@{DATABASE_HOSTNAME_Val}/{DATABASE_NAME_Val}' % urlquote(DATABASE_PASSWORD_Val)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()