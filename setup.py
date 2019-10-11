"""
Use this script to setup db.
"""
import pandas as pd
from tools import TableList
header = pd.read_csv("C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/header.csv")

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
path = "C:\\Users\\kbonefont.JER-PC-CLIMATE4\\Downloads\\AIM_data\\"
pathheight = r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\m_subset\height_subs.csv"

fname=os.path.join(path,'species_geojson.geojson')
try:
    df= gpd.read_file(fname)
except Exception as e:
    print(e)

query = 'SELECT * FROM gisdb.public."dataHeader";'
df2 = pd.read_sql(query, con=con)
header_old = pd.read_csv("C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/headerold.csv") # cant read
header = pd.read_csv("C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/header.csv")
height = pd.read_csv(r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\m_subset\height_subs.csv", low_memory=False)
height_old = pd.read_csv(r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\m_subset\height_subs_old.csv", low_memory=False)

spp = pd.read_csv(r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\m_subset\spp_subs.csv", low_memory=False)
spp_old =pd.read_csv(r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\spp_inventory_tall.csv", low_memory=False)

gap = pd.read_csv(r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\m_subset\gap_subs.csv", low_memory=False)
gapold = pd.read_csv(r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\gap_tall.csv", low_memory=False)


soil = pd.read_csv(r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\m_subset\soil_subs.csv", low_memory=False)

lpi = pd.read_csv(r"C:\Users\kbonefont.JER-PC-CLIMATE4\Downloads\AIM_data\m_subset\lpi_subs.csv", low_memory=False)


h_h_keydiff = set(height.PrimaryKey).difference(header.PrimaryKey)
g_h_keydiff = set(gap.PrimaryKey).difference(header.PrimaryKey)
gapold_hkeydiff = set(gapold.PrimaryKey).difference(header.PrimaryKey)
sp_hkeydiff = set(spp.PrimaryKey).difference(header.PrimaryKey)
spp_olddiff = set(spp_old.PrimaryKey).difference(header.PrimaryKey)
soil_hkeydiff = set(soil.PrimaryKey).difference(header.PrimaryKey)
lpi_hkeydiff = set(lpi.PrimaryKey).difference(header.PrimaryKey)


whereh_h = height.PrimaryKey.isin(h_h_keydiff)

whereg_h = gap.PrimaryKey.isin(g_h_keydiff)
whereg_hold = gapold.PrimaryKey.isin(gapold_hkeydiff)

wheresp_h = spp.PrimaryKey.isin(sp_hkeydiff)
wheresp_hold = spp_old.PrimaryKey.isin(spp_olddiff)

wheresoil_h = soil.PrimaryKey.isin(soil_hkeydiff)
wherelpi_h = lpi.PrimaryKey.isin(lpi_hkeydiff)

height[whereh_h].shape
gap[whereg_h].shape
gapold[whereg_hold].shape

spp[wheresp_h].shape
spp_old[wheresp_hold].shape

soil[wheresoil_h].shape
lpi[wherelpi_h].shape

height[whereh_h].to_csv('height_pks_missing_onheader.csv')
gap[whereg_h].to_csv('gap_pks_missing_onheader.csv')
spp[wheresp_h].to_csv('spp_pks_missing_onheader.csv')
soil[wheresoil_h].to_csv('soil_pks_missing_onheader.csv')
lpi[wherelpi_h].to_csv('lpi_pks_missing_onheader.csv')

key_diff = set(df.PrimaryKey).difference(header.PrimaryKey)
where_diff = df.PrimaryKey.isin(key_diff)
dfnew.shape
dfnew = df.copy(deep=True)
df[where_diff].shape
df[where_diff].to_csv('missing_geopk.csv')
