"""
Use this script to setup db.
"""
from tools import TableList

table_list = TableList()
table_list.pull_names()
table_list._table_list__names # <= list that holds current postgres db tables



# drops all foreign keys so tables can be dropped
from tools import drop_foreign_keys
for table in table_list._table_list__names:
    drop_foreign_keys(str(table))

# drops all public tables found
from temp_tools import drop_tbl
for table in table_list._table_list__names:
    drop_table(table)

# all table schemas created simultaneously except those w geometry
from tools import create_tbles
create_tbls() 

# data ingestion
from tools import tbl_ingest
table_ingest() 

# optional function to drop specific tables
from tools import drp_ind2
drp_ind2(None, None) 

# indicator ingestion
from tools import indicator_tables
ind_tbls('spe')
ind_tbls('ind')
