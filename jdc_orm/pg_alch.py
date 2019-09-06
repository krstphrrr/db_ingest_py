
from sqlalchemy import Column, String, Integer, Date
from base import Base


dbstr='posgresql+psycopg2://kris:JDC@1912!@jornada-ldc2.jrn.nmsu.edu:5432/gisdb'

# creating header table

from table.header import dataHeader
# dataHeader.__table__.create()
from common.base import jdc_db
opn = jdc_db()
print(dir(opn))
opn.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
