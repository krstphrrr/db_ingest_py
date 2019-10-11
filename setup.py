"""
Use this script to setup db.
"""
import pandas as pd
from tools import TableList

header.columns


table_list = TableList()
table_list.pull_names()
table_list._TableList__names # <= list that holds current postgres db tables



# drops all foreign keys so tables can be dropped
from tools import drop_foreign_keys
for table in table_list._TableList__names:
    drop_foreign_keys(str(table))

# drops all public tables found
from tools import drop_table
for table in table_list._TableList__names:
    drop_table(table)

# all table schemas created simultaneously except those w geometry
from tools import create_tbls
create_tbls()

# data ingestion
from tools import table_ingest
table_ingest()

# optional function to drop specific tables
from tools import drop_indicator

drop_indicator('geo', 1)

# indicator ingestion
from tools import indicator_tables
indicator_tables('spe')
# indicator_tables('ind')


import re,os, psycopg2
from configparser import ConfigParser
import pandas as pd
from tools import config
params = config()
con = psycopg2.connect(**params)
cur = con.cursor()
cur.close()
# strng = 'geoInd'
# for item in table_list._TableList__names:
#     print(list(filter(None,re.split('([a-z]+)(?=[A-Z])|([A-Z][a-z]+)',item))))

import geopandas as gpd

fname=os.path.join(path,'species_geojson.geojson')
try:
    df= gpd.read_file(fname)
except Exception as e:
    print(e)

query = 'SELECT * FROM gisdb.public."dataHeader";'
df2 = pd.read_sql(query, con=con)


key_diff = set(df.PrimaryKey).difference(header.PrimaryKey)
where_diff = df.PrimaryKey.isin(key_diff)
dfnew.shape
dfnew = df.copy(deep=True)
df[where_diff].shape
df[where_diff].to_csv('missing_geopk.csv')
