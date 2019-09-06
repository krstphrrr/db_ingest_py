
import os,psycopg2, sqlalchemy

import os
from sqlalchemy.engine import url as sa_url
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST')

class db_mod(object):
    _instance = None

    def __new__(cls):

        if cls._instance is None: # if empty, self
            cls._instance = object.__new__(cls)

            db_config = {'dbname': 'gisdb', 'host': os.environ.get('DB_HOST'),
                     'password': os.environ.get('DB_PASS'), 'port': 5432, 'user': os.environ.get('DB_USER')}

            try: # every instantiation = opens connection
                print('connecting to PostgreSQL database...')
                connection = db_mod._instance.connection = psycopg2.connect(**db_config)
                cursor = db_mod._instance.cursor = connection.cursor()
                cursor.execute('SELECT VERSION()')
                db_version = cursor.fetchone()

            except Exception as error: # if not, prints
                print('Error: connection not established {}'.format(error))
                db_mod._instance = None

            else:
                print('connection established\n{}'.format(db_version[0]))

        return cls._instance

    def __init__(self):
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def drop_fk(tablename):
        key_str = "{}_PrimaryKey_fkey".format(str(tablename))

        cur1.execute(sql.SQL('ALTER TABLE gisdb.public.{0} DROP CONSTRAINT IF EXISTS {1}').format(sql.Identifier(fk_tbl),sql.Identifier(key_str))  )

    def cleanup(self):
        cur = self.connection.cursor()
        qry = cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        table_list = qry.fetchall()
        t_list=[]
        for tab in table_list:
            while t_list.append(re.search(r"\(\'(.*?)\'\,\)",str(tab)).group(1)):
                cur.execute(sql.SQL("DROP TABLE IF EXISTS gisdb.public.{0}").format(sql.Identifier(tab))
                )


newdb = db_mod()
newdb.cleanup()

##
db_connect_url = sa_url.URL(
drivername="postgresql",
username =db_user,
password=db_password,
host=db_host,
port=5432,
database="gisdb")

engine = create_engine(db_connect_url)

from header import dataHeader
