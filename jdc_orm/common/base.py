# coding=utf-8

import os
import psycopg2
import logging
import sys
from sqlalchemy.engine import url as sa_url
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection parameters
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST')

# connection credentials
db_connect_url = sa_url.URL(
    drivername="postgresql",
    username =db_user,
    password=db_password,
    host=db_host,
    port=5432,
    database="gisdb")

# sqlalchemy engine
engine = create_engine(db_connect_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class jdc_db():
    """ db connection class """
    def __init__(self):
        self.conn = None

    def dbconn(self):
        db_config = {'dbname': 'gisdb', 'host': os.environ.get('DB_HOST'),
                 'password': os.environ.get('DB_PASS'), 'port': 5432, 'user': os.environ.get('DB_USER')}

        try:
            """connect to the db"""
            if(self.conn is None):
                self.conn = psycopg2.connect(**db_config)

        except psycopg2.DatabaseError as e:
            logging.error(e)
            sys.exit()
        finally:
            logging.info('Connection opened.')


    def run_query(self, query):
        """run query"""
        try:
            self.dbconn()
            with self.conn.cursor() as cur:
                if 'SELECT' in query:
                    records = []
                    cur.execute(query)
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)
                    cur.close()
                    return records
                else:
                    result = cur.execute(query)
                    self.conn.commit()
                    affected = f"{cur.rowcount} rows affected"
                    cur.close()
                    return affected
        except psycopg2.DatabaseError as e:
                    print(e)
        finally:
            if self.conn:
                self.conn.close()
                logging.info('DB connection closed!')

ok = jdc_db()
ok.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
ok.run_query('SELECT * FROM gisdb.public."dataHeader" LIMIT 10')
