import psycopg2
import pandas as pd
import csv
import os
import gdaltools



# reading up env. variables

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST')

# table ingestion from csv, null values are 'NA'
# still requires table schema

conn = psycopg2.connect(dbname="gisdb",
                        user=db_user,
                        password=db_password,
                        port="5432",
                        host=db_host)
cur = conn.cursor()

# header table: drop constraints > drop table > create schema > populate
cur.execute("""
ALTER TABLE gisdb.public."dataHeader" DROP CONSTRAINT IF EXISTS header_tall_pkey CASCADE;
DROP TABLE IF EXISTS gisdb.public."dataHeader";
DROP TABLE IF EXISTS gisdb.public."dataGap";
DROP TABLE IF EXISTS gisdb.public."dataHeight";
DROP TABLE IF EXISTS gisdb.public."dataSpeciesInventory";
DROP TABLE IF EXISTS gisdb.public."dataSoilStability";""")

cur.execute("""
DROP TABLE IF EXISTS gisdb.public."dataHeader";
CREATE TABLE gisdb.public."dataHeader"(
  "PrimaryKey" VARCHAR(100) PRIMARY KEY,
  "SpeciesState" VARCHAR(2),
  "PlotID" TEXT,
  "PlotKey" VARCHAR(50),
  "DBKey" TEXT,
  "EcologicalSiteId" VARCHAR(50),
  "Latitude_NAD83" NUMERIC,
  "Longitude_NAD83" NUMERIC,
  "State" VARCHAR(2),
  "County" VARCHAR(50),
  "DateEstablished" DATE,
  "DateLoadedInDb" DATE,
  "ProjectName" TEXT,
  "Source" TEXT,
  "LocationType" VARCHAR(20),
  "DateVisited" DATE,
  "Elevation" NUMERIC,
  "PercentCoveredByEcoSite" NUMERIC);
""")
conn.commit()
# Schema

# populate
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/header.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataHeader\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
conn.commit()
