

# importing connection/query tool
from common.base import jdc_db
# instantiating tool
ok = jdc_db()
# querying user tables just in case
ok.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")


ok.run_query('DROP TABLE gisdb.public."dataHeader"')

# creating header table

from table.header import dataHeader
dataHeader.__table__.create()
