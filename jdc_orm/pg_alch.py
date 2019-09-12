
## setup script
from temp_tools import tbl_list

tlist = tbl_list()
tlist.all()
tlist.t_list

###########################

# drops all foreign keys so tables can be dropped
from temp_tools import drop_fk
for tbl in tlist.t_list:
    drop_fk(str(tbl))

# drops all public tables found
from temp_tools import drop_tbl
for tbl in tlist.t_list:
    drop_tbl(tbl)

# all table schemas created simultaneously except those w geometry
from temp_tools import create_tbls
create_tbls() # needs actual names

# data ingestion
from temp_tools import tbl_ingest
tbl_ingest() # needs ok after each successful csv ingest

# drop geo table if exists
from temp_tools import drp_ind2
drp_ind2('Gap') # would be nice to choose which substring to match
drp_ind2('geo', 0) # done

# indicator ingestion
from temp_tools import ind_tbls
ind_tbls('spe')
