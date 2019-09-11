
## setup script
from temp_tools import tbl_list

tlist = tbl_list()
tlist.all()
tlist.t_list

###########################

from temp_tools import drop_fk
for tbl in tlist.t_list:
    drop_fk(str(tbl))


from temp_tools import drop_tbl
for tbl in tlist.t_list:
    drop_tbl(tbl)



# all table schemas created simultaneously except those w geometry
from temp_tools import create_tbls
create_tbls()

from common.base import engine
from __init__ import conn,cur


# data ingestion
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/header.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataHeader\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
    conn.commit()


with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/gap_subs.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataGap\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
    conn.commit()
    # conn.close()

gapdf.head()

import pandas as pd

gapdf = pd.read_csv('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/gap_subs.csv', low_memory = False)
gapdf.shape
# 1,369,642 rows

gapdf.columns

for col in gapdf.columns:
    print(col,gapdf[col].nunique())
