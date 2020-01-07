"""
Use this script to setup db.
"""
import os
os.environ

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

"""

from tools import table_ingest
table_ingest()

# optional function to drop specific tables
from tools import drop_indicator
drop_indicator('geo', 0)

# indicator ingestion
from tools import indicator_tables
indicator_tables('spe')
