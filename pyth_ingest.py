import psycopg2
import pandas as pd
import csv
import os
import gdaltools
import gdal

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


# Schema - header
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
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/header.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataHeader\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
conn.commit()

# schema - gap

cur.execute("""
DROP TABLE IF EXISTS gisdb.public."dataGap";
CREATE TABLE gisdb.public."dataGap"(
  "LineKey" VARCHAR(100),
  "RecKey" VARCHAR(100),
  "DateModified" DATE,
  "FormType" TEXT,
  "FormDate" DATE,
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "Direction"NUMERIC,
  "Measure" INT,
  "LineLengthAmount" NUMERIC,
  "GapMin" NUMERIC,
  "GapData" INT,
  "PerennialsCanopy" INT,
  "AnnualGrassesCanopy" INT,
  "AnnualForbsCanopy" INT,
  "OtherCanopy" INT,
  "Notes" TEXT,
  "NoCanopyGaps" INT,
  "NoBasalGaps" INT,
  "DateLoadedInDb" DATE,
  "PerennialsBasal" INT,
  "AnnualGrassesBasal" INT,
  "AnnualForbsBasal" INT,
  "OtherBasal" INT,
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "SeqNo" TEXT,
  "RecType" TEXT,
  "GapStart" NUMERIC,
  "GapEnd" NUMERIC,
  "Gap" NUMERIC,
  "Source" TEXT);
""")
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/gap_subs.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataGap\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
conn.commit()

# schema -  lpi

cur.execute("""
DROP TABLE IF EXISTS gisdb.public."dataLPI";
CREATE TABLE gisdb.public."dataLPI"(
  "LineKey" VARCHAR(100),
  "RecKey" VARCHAR(100),
  "DateModified" DATE,
  "FormType" TEXT,
  "FormDate" DATE,
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "Direction" VARCHAR(50),
  "Measure" INT,
  "LineLengthAmount" NUMERIC,
  "SpacingIntervalAmount" NUMERIC,
  "SpacingType" TEXT,
  "HeightOption" TEXT,
  "HeightUOM" TEXT,
  "ShowCheckbox" INT,
  "CheckboxLabel" TEXT,
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "PointLoc" NUMERIC,
  "PointNbr" INT,
  "ShrubShape" TEXT,
  "layer" TEXT,
  "code" TEXT,
  "chckbox" INT,
  "Source" TEXT);
""")
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/lpi_subs.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataLPI\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
cur.execute("ALTER TABLE gisdb.public.\"dataLPI\" DROP COLUMN \"HeightOption\", DROP COLUMN \"HeightUOM\", DROP COLUMN \"ShowCheckbox\";")
conn.commit()
conn.commit()

# schema - height

cur.execute("""
DROP TABLE IF EXISTS gisdb.public."dataHeight";
CREATE TABLE gisdb.public."dataHeight"(
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "PointLoc" NUMERIC,
  "PointNbr" INT,
  "RecKey" VARCHAR(100),
  "Height" NUMERIC,
  "Species" TEXT,
  "Chkbox" INT,
  "type" TEXT,
  "GrowthHabit_measured" TEXT,
  "LineKey" VARCHAR(100),
  "DateModified" DATE,
  "FormType" TEXT,
  "FormDate" DATE,
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "Direction" VARCHAR(100),
  "Measure" INT,
  "LineLengthAmount" NUMERIC,
  "SpacingIntervalAmount" NUMERIC,
  "SpacingType" TEXT,
  "HeightOption" TEXT,
  "HeightUOM" TEXT,
  "ShowCheckbox" INT,
  "CheckboxLabel" TEXT,
  "Source" TEXT,
  "UOM" TEXT)
""")
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/height_subs.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataHeight\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
cur.execute("ALTER TABLE gisdb.public.\"dataHeight\" DROP COLUMN \"SpacingIntervalAmount\", DROP COLUMN \"SpacingType\", DROP COLUMN \"ShowCheckbox\", DROP COLUMN \"UOM\";")
conn.commit()

# schema - soil stability

cur.execute("""
DROP TABLE IF EXISTS gisdb.public."dataSoilStability";
CREATE TABLE gisdb.public."dataSoilStability"(
  "PlotKey" VARCHAR(100),
  "RecKey" VARCHAR(100),
  "DateModified" DATE,
  "FormType" TEXT,
  "FormDate" DATE,
  "LineKey" VARCHAR(100),
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "SoilStabSubSurface" INT,
  "Notes" TEXT,
  "DateLoadedInDb" DATE,
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "Position" INT,
  "Line" VARCHAR(50),
  "Pos" VARCHAR(50),
  "Veg" TEXT,
  "Rating" INT,
  "Hydro" INT,
  "Source" TEXT);
""")
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/soil_subs.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataSoilStability\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
cur.execute("ALTER TABLE gisdb.public.\"dataSoilStability\" DROP COLUMN \"FormType\";")
conn.commit()

# schema - species inventory

cur.execute("""
DROP TABLE IF EXISTS gisdb.public."dataSpeciesInventory";
CREATE TABLE gisdb.public."dataSpeciesInventory"(
  "LineKey" VARCHAR(100),
  "RecKey" VARCHAR(100),
  "DateModified" DATE,
  "FormType" TEXT,
  "FormDate" DATE,
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "SpecRichMethod" INT,
  "SpecRichMeasure" INT,
  "SpecRichNbrSubPlots" INT,
  "SpecRich1Container" INT,
  "SpecRich1Shape" INT,
  "SpecRich1Dim1" NUMERIC,
  "SpecRich1Dim2" NUMERIC,
  "SpecRich1Area" NUMERIC,
  "Notes" TEXT,
  "DateLoadedInDb" DATE,
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "Species" TEXT,
  "Source" TEXT,
  "Density" INT);
""")
with open('C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/m_subset/spp_subs.csv','r') as f:
    cur.copy_expert("COPY gisdb.public.\"dataSpeciesInventory\" FROM STDIN WITH CSV HEADER NULL \'NA\'" ,f)
cur.execute("ALTER TABLE gisdb.public.\"dataSpeciesInventory\" DROP COLUMN \"FormType\";")
conn.commit()


ogr2ogr -f "PostgreSQL" -a_srs "EPSG:4326" PG:"dbname=* user=* password=* host=* port=*" "source_data.json" -nln "source_data"

ogr = gdaltools.ogr2ogr()
ogr.set_encoding("UTF-8")
ogr.set_input("C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/species_geojson.geojson")
# requires gdal / osgeow4
gdaltools.Wrapper.BASEPATH = os.environ.get('GDAL_PATH')
ogr.geom_type = 'POINT'
con = gdaltools.PgConnectionString(host=db_host, port=5432, dbname="gisdb", schema="public", user=db_user, password=db_password)
ogr.set_output(con, table_name="geo_Spe", srs="EPSG:4326")

ogr.execute()

cur.execute('ALTER TABLE gisdb.public."geo_Spe" ADD CONSTRAINT geo_spe_fk FOREIGN KEY ("PrimaryKey") REFERENCES "dataHeader" ("PrimaryKey");')
