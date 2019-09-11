
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
create_tbls() # needs actual names




# data ingestion
from temp_tools import tbl_ingest

tbl_ingest() # needs ok after each successful csv ingest

# indicator tables schema + ingestion
