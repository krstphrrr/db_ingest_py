# coding=utf-8

import os
from sqlalchemy.engine import url as sa_url
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST')

db_connect_url = sa_url.URL(
drivername="postgresql",
username =db_user,
password=db_password,
host=db_host,
port=5432,
database="gisdb")

engine = create_engine(db_connect_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()
