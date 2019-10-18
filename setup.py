"""
Use this script to setup db.
"""
import pandas as pd
import psycopg2
from tools import config

from tools import TableList

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
"""
- if data to be ingested is Rdata,
change into csv.
- check if csv fields are the same the
schema in the script. if not, add the new fields
and their field type.
- check if new fields are true

DateLoadedInDb is 2016 in header

"""

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
import pandas as pd
fname=os.path.join(path,'species_geojson.geojson')
df = pd.read_csv(r'C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\header.csv', low_memory=False)

try:
    df= gpd.read_file(fname)
except Exception as e:
    print(e)

query = 'SELECT * FROM gisdb.public."dataHeader";'
df2 = pd.read_csv(r'C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\m_subset\height_subs.csv', low_memory=False)

len(df.PrimaryKey.unique())
len(df2.PrimaryKey.unique())
any(df2.PrimaryKey.isin(key_diff))

key_diff = set(df.PrimaryKey).difference(df.PrimaryKey)
len(key_diff)



where_diff = df2.PrimaryKey.isin(key_diff2)


df[where_diff].shape
df[where_diff].to_csv('missing_geopk.csv')
