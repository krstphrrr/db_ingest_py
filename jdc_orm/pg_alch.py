
# importing connection/query tool
from common.base import jdc_db

# dropping fk's

# dropping tables
ok = jdc_db()
ok.run_query('DROP TABLE IF EXISTS gisdb.public."dataGap"')
ok.run_query('DROP TABLE IF EXISTS gisdb.public."dataHeader"')



# creating header table
from table.header import dataHeader
from common.base import engine
from __init__ import conn,cur

dataHeader.__table__.create(engine)
# header table data ingestion

with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/header.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataHeader\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
    conn.commit()
    # conn.close()

#test: do tables EXIST
ok = jdc_db() # instantiation
ok.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")


# creating gap tables

from table.gap import dataGap

dataGap.__table__.create(engine)

with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/gap_subs.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataGap\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
    conn.commit()
    # conn.close()


import pandas as pd

gapdf = pd.read_csv('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/gap_subs.csv', low_memory = False)
gapdf.shape
# 1,369,642 rows

gapdf.columns

for col in gapdf.columns:
    print(col,gapdf[col].nunique())
