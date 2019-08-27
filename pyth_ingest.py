import psycopg2
import pandas as pd
import csv
import os

# reading up env. variables

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST')

# table ingestion from csv, null values are 'NA'

conn = psycopg2.connect(dbname="postgres", user=db_user, password=db_password, port="5432", host=db_host)
cur = conn.cursor()
cur.execute("ALTER TABLE header_tall DROP CONSTRAINT IF EXISTS header_tall_pkey CASCADE")
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/header.csv','r') as f:
    cur.copy_expert("COPY header_tall FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
conn.commit()
