# coding=utf-8

import os
import psycopg2
import logging
import sys
from sqlalchemy.engine import url as sa_url
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection class to construct engine url
class conx():

    dbu = 'DB_USER'
    dbp = 'DB_PASS'
    dbh = 'DB_HOST'

    # dburl= u.print()
    def __init__(self, url):
       import os
       from sqlalchemy.engine import url as sa_url
       self.db_user = os.environ.get(self.dbu)
       self.db_password = os.environ.get(self.dbp)
       self.db_host = os.environ.get(self.dbh)
       self.db_url = sa_url.URL(drivername="postgresql", username =self.db_user, password=self.db_password, host=self.db_host, port=5432, database=url)


db = conx("gisdb")

# got url > drop url
# sqlalchemy engine
engine = create_engine(db.db_url)

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
