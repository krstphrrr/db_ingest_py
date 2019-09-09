
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


# creating gap tables
from sqlalchemy import *
metadata = MetaData()
metadata.clear()
dataGap.metadata.clear()
from table.gap import dataGap
dataGap.__table__.create(engine)



import pandas as pd

gapdf = pd.read_csv('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/gap_subs.csv', low_memory = False)
gapdf.shape
# 1,369,642 rows

gapdf.columns


gapdf.groupby('LineKey').nunique()

str(gapdf['LineKey'].columns)
for col in gapdf.columns:
    print(col,gapdf[col].nunique())
gapdf['LineKey'].nunique()
