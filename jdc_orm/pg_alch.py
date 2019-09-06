
# importing connection/query tool
from common.base import jdc_db

# creating header table
from table.header import dataHeader
from common.base import engine
from __init__ import conn,cur

dataHeader.__table__.create(engine)
# header table data ingestion
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/header.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataHeader\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
    conn.commit()

#test: do tables EXIST
ok = jdc_db() # instantiation
ok.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
