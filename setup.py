"""
Use this script to setup db.
"""

import pandas as pd
import psycopg2
from tools import config

from tools import TableList
from tools import db
import os
import pandas as pd



"""
check tables up in postgres
"""
table_list = TableList()
table_list.pull_names()
table_list._TableList__names # <= list that holds current postgres db tables


"""
1 . drop all foreign keys; FK constraints prevent dropping tables
    avoids dropping FK for: groups, users, pages

issues:
- any errors with connection during this function would return
"connection already closed.." and it would not run thereafter.
Wrapped it in a try block and 'on exception', the error gets
printed and the connection creates a new cursor which would run.
"""
from tools import drop_foreign_keys
for table in table_list._TableList__names:
    if table.find('user')!=-1 or table.find('groups')!=-1 or table.find('pages')!=-1:
        pass
    else:
        drop_foreign_keys(table)



"""
2. drop all tables
    avoids dropping the groups, users and pages tables
issues:
- down where -geo tables are ingested, there was a
mistake in the foreign key name given: 'geoInd_PrimaryKey_fkey'
instead of 'geoIndicators_PrimaryKey_fkey'
"""
from tools import drop_table
for table in table_list._TableList__names:
    if table.find('user')!=-1 or table.find('groups')!=-1 or table.find('pages')!=-1:
        pass
    else:
        drop_table(table)

# all table schemas created simultaneously except those w geometry
from tools import create_tbls
create_tbls()

# data ingestion
"""
notes:
- if data to be ingested is Rdata,
change into csv.
- check if csv fields are the same the
schema in the script. if not, add the new fields
and their field type.
- check if new fields are true

4. check which csv's are in the directory. ideally, only
those to be ingested should be there and appear only once. this avoids
having to be hard-coding names into the function and files.
issues:
- years in string format: "2016" instead of mm:dd:yy etc.
- replace in excel file until better method appears

- check if columns in csv are the same in db
"""


from tools import headeringest
headeringest()

from tools import table_ingest
table_ingest()

# optional function to drop specific tables
from tools import drop_indicator
drop_indicator('geo', 0)

# indicator ingestion
import geopandas as gpd
gdf = gpd.read_file(r"C:\Users\kbonefont\Desktop\data\geoInd.geojson")
from tools import indicator_tables
indicator_tables('ind')
