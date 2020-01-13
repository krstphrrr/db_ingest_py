"""
This script contains functions and class methods drto set up the server using
psycopg2. Across the whole script, cur and con are shorthand for cursor and
connection objects respectively.

1. config and geoconfig, parse information inside a local ini file to be
used by other functions that connect to the server.

2. class TableList queries the server using the pull_names method and
populates an internal attribute (__names) with the names of all the tables
currently on the server.

2. drop_foreign_keys executes a 'ALTER TABLE..DROP FOREIGN KEY IF EXISTS..'
SQL query. This enables the pg table to be modified as its constraints have
been dropped.

3. drop_tables executes an 'DROP TABLE IF EXISTS..' SQL query. Requires table
constraints to be dropped.

4. create_tables creates table schemas using a 'CREATE TABLE..' query.

5. table_ingest batch uploads all the csv into pg table schemas using the
copy_expert/insert function.

6. drop_indicator is used for the selective dropping of tables. It splits up table
names into two: ex. dataHeader = 'data' + 'Header', so the user chooses by which
string to filter and which position to filter at.

7. column_name_changer changes column names on a chosen table.

8. indicator_tables creates and ingests tables with a geometry field.


"""

from configparser import ConfigParser
from psycopg2 import connect, sql
from psycopg2.pool import SimpleConnectionPool
from pandas import read_sql_query
from psycopg2 import connect, sql
from os import chdir, getcwd
from os.path import abspath, join
import pandas as pd
from os import getcwd
from os.path import normpath,join, splitext
import pandas as pd
import os

path = os.environ['DC_DATA']
def config(filename='database.ini', section='postgresql'):
    """
    Uses the configpaser module to read .ini and return a dictionary of
    credentials
    """
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(
        section, filename))

    return db



def geoconfig(filename='database.ini', section='geo'):
    """
    Same as config but reads another section.
    """
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(
        section, filename))
    return db

class db:
    params = config()
    # str = connect(**params)
    str_1 = SimpleConnectionPool(minconn=1,maxconn=10,**params)
    str = str_1.getconn()

    def __init__(self):

        self._conn = connect(**params)
        self._cur= self._conn.cursor()


class TableList():
    """
    This class creates a list of tables currently in the server.
    Connection credentials inside .ini file. pull_names method
    extracts table names and assigns them to the __names class
    attribute, which initially is just an empty list.
    """
    __names = []
    __seen = None

    def pull_names(self):

        import re

        con = db.str
        cur = con.cursor()
        # looking up all user-defined tables in db
        try:
            cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;""")
            query_results = cur.fetchall()

            for table in query_results:
                self.__seen = set(self.__names)
                if table not in self.__seen:
                    self.__seen.add(re.search(r"\(\'(.*?)\'\,\)",
                    str(table)).group(1))
                    self.__names.append(re.search(r"\(\'(.*?)\'\,\)",
                    str(table)).group(1))
        except Exception as e:
            print(e)
            con = db.str
            cursor=con.cursor()



def drop_foreign_keys(table):
    """
    This function drops all constraints in a table. It relies on
    postgresql's default naming convention for foreign key constraints.
    Foreign keys = 'TableName_ColumnName_fkey'. Using a table name
    supplied as a function argument, it creates a foreign key name and it
    populates a query with both the constraint name and table name.
    """
    import re
    con = db.str
    cur = con.cursor()

    key_str = "{}_PrimaryKey_fkey".format(str(table))
    print('try: dropping keys...')
    try:
        cur.execute(
            sql.SQL("""ALTER TABLE gisdb.public.{0}
                   DROP CONSTRAINT IF EXISTS {1}""").format(
                   sql.Identifier(table),
                   sql.Identifier(key_str))
        )
    except Exception as e:
        print(e)
        con = db.str
        cur = con.cursor()
    print(f"Foreign keys on {table} dropped")
    con.commit()


def drop_table(table):
    """
    Drops the table used as an argument executing a
    "DROP TABLE IF EXISTS.." query.
    """
    import re
    con = db.str
    cur = con.cursor()
    try:
        cur.execute(
            sql.SQL('DROP TABLE IF EXISTS gisdb.public.{0}').format(
                     sql.Identifier(table))
        )
        con.commit()
    except exception as e:
        print(e)
        con = db.str
        cur = con.cursor()
    print(f"table {table} has been dropped")


def create_tbls():
    """
    Opens a connection, loops through a tuple of "CREATE TABLE.." commands
    and closes the connection.
    """
    commands = (
    """ CREATE TABLE "dataHeader"(
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
    "source" TEXT,
    "LocationType" VARCHAR(20),
    "DateVisited" DATE,
    "Elevation" NUMERIC,
    "PercentCoveredByEcoSite" NUMERIC);""",

    """CREATE TABLE "dataGap"(
    "LineKey" VARCHAR(100),
    "RecKey" VARCHAR(100),
    "DateModified" DATE,
    "FormType" TEXT,
    "FormDate" DATE,
    "Observer" TEXT,
    "Recorder" TEXT,
    "DataEntry" TEXT,
    "DataErrorChecking" TEXT,
    "Direction" NUMERIC,
    "Measure" NUMERIC,
    "LineLengthAmount" NUMERIC,
    "GapMin" NUMERIC,
    "GapData" NUMERIC,
    "PerennialsCanopy" NUMERIC,
    "AnnualGrassesCanopy" NUMERIC,
    "AnnualForbsCanopy" NUMERIC,
    "OtherCanopy" NUMERIC,
    "Notes" TEXT,
    "NoCanopyGaps" NUMERIC,
    "NoBasalGaps" NUMERIC,
    "DateLoadedInDb" DATE,
    "PerennialsBasal" NUMERIC,
    "AnnualGrassesBasal" NUMERIC,
    "AnnualForbsBasal" NUMERIC,
    "OtherBasal" NUMERIC,
    "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
    "DBKey" TEXT,
    "SeqNo" TEXT,
    "RecType" TEXT,
    "GapStart" NUMERIC,
    "GapEnd" NUMERIC,
    "Gap" NUMERIC,
    "source" TEXT,
    "State" TEXT,
    "PlotKey" TEXT);""",

    """ CREATE TABLE "dataLPI"(
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
    "Measure" NUMERIC,
    "LineLengthAmount" NUMERIC,
    "SpacingIntervalAmount" NUMERIC,
    "SpacingType" TEXT,
    "HeightOption" TEXT,
    "HeightUOM" TEXT,
    "ShowCheckbox" NUMERIC,
    "CheckboxLabel" TEXT,
    "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
    "DBKey" TEXT,
    "PointLoc" NUMERIC,
    "PointNbr" NUMERIC,
    "ShrubShape" TEXT,
    "layer" TEXT,
    "code" TEXT,
    "chckbox" INT,
    "source" TEXT);""",

    """ CREATE TABLE "dataHeight"(
    "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
    "DBKey" TEXT,
    "PointLoc" NUMERIC,
    "PointNbr" NUMERIC,
    "RecKey" VARCHAR(100),
    "Height" NUMERIC,
    "Species" TEXT,
    "Chkbox" NUMERIC,
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
    "Measure" NUMERIC,
    "LineLengthAmount" NUMERIC,
    "SpacingIntervalAmount" NUMERIC,
    "SpacingType" TEXT,
    "HeightOption" TEXT,
    "HeightUOM" TEXT,
    "ShowCheckbox" NUMERIC,
    "CheckboxLabel" TEXT,
    "source" TEXT,
    "UOM" TEXT);""",

    """ CREATE TABLE "dataSoilStability"(
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
    "SoilStabSubSurface" NUMERIC,
    "Notes" TEXT,
    "DateLoadedInDb" DATE,
    "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
    "DBKey" TEXT,
    "Position" NUMERIC,
    "Line" VARCHAR(50),
    "Pos" VARCHAR(50),
    "Veg" TEXT,
    "Rating" NUMERIC,
    "Hydro" NUMERIC,
    "source" TEXT);""",

    """ CREATE TABLE "dataSpeciesInventory"(
    "LineKey" VARCHAR(100),
    "RecKey" VARCHAR(100),
    "DateModified" DATE,
    "FormType" TEXT,
    "FormDate" DATE,
    "Observer" TEXT,
    "Recorder" TEXT,
    "DataEntry" TEXT,
    "DataErrorChecking" TEXT,
    "SpecRichMethod" NUMERIC,
    "SpecRichMeasure" NUMERIC,
    "SpecRichNbrSubPlots" NUMERIC,
    "SpecRich1Container" NUMERIC,
    "SpecRich1Shape" NUMERIC,
    "SpecRich1Dim1" NUMERIC,
    "SpecRich1Dim2" NUMERIC,
    "SpecRich1Area" NUMERIC,
    "Notes" TEXT,
    "DateLoadedInDb" DATE,
    "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
    "DBKey" TEXT,
    "Species" TEXT,
    "source" TEXT,
    "SpeciesCount" VARCHAR(100),
    "Density" NUMERIC,
    "Plotkey" TEXT);
    """
    )
    conn = None
    try:
        print('Connecting...')
        conn = db.str
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
            print("Tables created!")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is None:
            conn.close()

#####


def queryfun(tablename, file):
    from psycopg2 import sql
    con = db.str
    cur = con.cursor()

    try:
        cur.copy_expert(f'COPY gisdb.public."{tablename}" FROM STDIN WITH CSV HEADER NULL \'NA\'', file)

        cur.execute(
         sql.SQL("""
         ALTER TABLE gisdb.public.{0}
         DROP COLUMN IF EXISTS "DateLoadedInDb"
         """).format(
         sql.Identifier(tablename)))

        cur.execute(
         sql.SQL("""
         ALTER TABLE gisdb.public.{0}
         ADD COLUMN "DateLoadedInDb" DATE""").format(
         sql.Identifier(tablename)))

        cur.execute(
         sql.SQL("""
         UPDATE gisdb.public.{0}
         SET "DateLoadedInDb"=now()""").format(
         sql.Identifier(tablename)) )
    except Exception as e:
        print(e)
        con = db.str
        cur = con.cursor()
    con.commit()


def prequery(tablename):
    """
    1.
    """
    pkmiss = dict()


    # print("reading data..")
    chosenvsdf = pd.read_csv(normpath(join(f'{path}',tablename)), encoding='utf-8', low_memory=False)
    header = pd.read_sql_query('SELECT * FROM gisdb.public."dataHeader"', db.str)
    key_diff = set(chosenvsdf.PrimaryKey).difference(header.PrimaryKey)
    where_diff = chosenvsdf.PrimaryKey.isin(key_diff)

    if len(key_diff)!=0:
        tablenam = f'{tablename}'.split(".csv")[0]
        # print([i for i in self.chosenvsdf[where_diff].PrimaryKey.unique()])
        # saving the badone
        badones = "missingpks"
        print(f"checking primary key differences for {tablenam}...")

        # creating string w dictionary

        pkmiss.setdefault(join(f'{tablenam}',"missing"),[])

        if os.path.exists(os.path.join(path,badones)):
            pass
        else:
            os.mkdir(os.path.join(path,badones))

        if not [i for i in chosenvsdf[where_diff].PrimaryKey.unique()]:
            print("No primary key differences between csv and header")
        else:
            for item in [i for i in chosenvsdf[where_diff].PrimaryKey.unique()]:
                if type(item)!=float:
                    pkmiss[os.path.join(f'{tablenam}',"missing")].append(item)

                else:
                    print("Float among the primary keys.")

            misspk_str =  os.path.join("missing primary keys :"+", ".join(pkmiss[os.path.join(f'{tablenam}',"missing")]))
            print(misspk_str)

        # saving  the goodones
        goodones = "good_csvs"

        if os.path.exists(os.path.join(path,goodones)):
            pass
        else:
            os.mkdir(os.path.join(path,goodones))

        print(f"saving {tablenam} csv with missing primarykeys in 'badones' folder...")
        chosenvsdf[where_diff].to_csv(os.path.join(os.path.join(path,badones)+"\\"+tablenam+"_pk_missingfromheader.csv"),index=False)
        good_df = chosenvsdf[~where_diff]
        good_na = good_df.fillna("NA")
        good_na = good_na.loc[:, ~good_na.columns.str.contains('^Unnamed')]
        # in case spp table has a bunch of extra fields
        for item in good_na.columns:
            spp_list =["SpecRich2Container", "SpecRich2Shape", "SpecRich2Dim1", "SpecRich2Dim2",
            "SpecRich2Area", "SpecRich3Container", "SpecRich3Shape", "SpecRich3Dim1", "SpecRich3Dim2",
            "SpecRich3Area", "SpecRich4Container", "SpecRich4Shape", "SpecRich4Dim1", "SpecRich4Dim2",
            "SpecRich4Area", "SpecRich5Container", "SpecRich5Shape", "SpecRich5Dim1", "SpecRich5Dim2",
            "SpecRich5Area", "SpecRich6Container", "SpecRich6Shape", "SpecRich6Dim1", "SpecRich6Dim2",
            "SpecRich6Area"]
            if item in spp_list:
                good_na = good_na.loc[:, ~good_na.columns.str.contains(item)]

        good_na.to_csv(join(join(path,goodones)+"\\"+tablenam+"_subs.csv"),index=False)
        print(f"good csv's saved for {tablenam} in 'good csvs' folder")
    else:
        print("no difference in primary keys")


def headeringest():
    """
    ingesting header first: in the next function, potential ingests
    are going to be compared against this header to find extra primary keys.
    """
    import os
    from os import getcwd
    path = os.environ['DC_DATA']
    str = "good_csvs"

    prefix = 'data'
    wd = getcwd()
    for file in os.listdir(path):
        if os.path.splitext(file)[1]=='.csv' and file.find('header')!=-1:

            with open(os.path.join(path,file),'r') as f:
                camelcase = os.path.join(prefix+'header'.capitalize())
                print("Ingesting header..")
                queryfun(camelcase, f)
                print("Header up.")

def table_ingest():
    """
    Reads csv data and uploads it into appropriate pg table.
    1. finds appropriate csv.
    2. does primarykey check
    3. saves two csvs: missing primary keys, and matching ones
    4. ingests matching ones
    """

    import os
    from os import getcwd
    path = os.environ['DC_DATA']
    str = "good_csvs"
    wd = getcwd()

    prefix = 'data'

    for file in os.listdir(path):
        if os.path.splitext(file)[1]=='.csv' and file.find('spp')!=-1:
            prequery(file)
            with open(os.path.join(path,str,os.path.splitext(file)[0]+'_subs.csv'),'r') as f:
                camelcase = os.path.join(prefix+'SpeciesInventory')
                print("Ingesting species inventory..")
                queryfun(camelcase, f)
                print("Species inventory up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('soil')!=-1:
            prequery(file)
            with open(os.path.join(path,str,os.path.splitext(file)[0]+'_subs.csv'),'r') as f:
                camelcase = os.path.join(prefix+'SoilStability')
                print("Ingesting soilstability..")
                queryfun(camelcase, f)
                print("soilstability up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('lpi')!=-1:
            prequery(file)
            with open(os.path.join(path,str,os.path.splitext(file)[0]+'_subs.csv'),'r') as f:
                camelcase = os.path.join(prefix+'LPI')
                print("Ingesting LPI..")
                queryfun(camelcase, f)
                print("LPI up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('height')!=-1:
            prequery(file)
            with open(os.path.join(path,str,os.path.splitext(file)[0]+'_subs.csv'),'r') as f:
                camelcase = os.path.join(prefix+'Height')
                print("Ingesting height..")
                queryfun(camelcase, f)
                print("height up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('gap')!=-1:
            prequery(file)
            with open(os.path.join(path,str,os.path.splitext(file)[0]+'_subs.csv'),'r') as f:
                camelcase = os.path.join(prefix+'Gap')
                print("Ingesting gap..")
                queryfun(camelcase, f)
                print("gap up.")



def drop_indicator(prefix,string_position):
    """
    Takes as arguments pg table prefix to filter through list of table names,
    and position in the camelcase names. It uses a "DROP TABLE IF EXISTS.."
    query to drop the table filtered through the user-defined string and
    position. Useful for dropping tables with a specific prefix in their
    name. ex.. data or geo
    """
    import re
    from psycopg2 import sql
    from tools import config
    from tools import TableList
    tlist = TableList()
    tlist.pull_names()

    string = "{}".format(str(prefix))

    for item in tlist._TableList__names:

        if list(filter(None, re.split('([a-z]+)(?=[A-Z])|([A-Z][a-z]+)', item)))[string_position] == string:
            try:
                print(item +' dropped')
                con = db.str
                cur = con.cursor()

                cur.execute(
                sql.SQL("DROP TABLE IF EXISTS gisdb.public.{};").format(
                sql.Identifier(item))
            )
                con.commit()
            except Exception as e:
                print(e)


def matcher(table,colstring):
    df = read_sql_query(sql.SQL('SELECT * FROM gisdb.public.{0} LIMIT 1').format(sql.Identifier(table)), db.str)
    # df = read_sql_query('SELECT * FROM gisdb.public."geospe" LIMIT 1', db.str)
    for item in df.columns:
        if item.lower()== f'{colstring}'.lower():
            return item

def column_name_changer(table_name,which_column,newname):
    """
    Takes table name, column name and new column name to change a column's
    name.
    """
    con = db.str
    cur = con.cursor()

    cur.execute(
        sql.SQL("""
        ALTER TABLE gisdb.public.{0}
        RENAME COLUMN {1} TO {2}""").format(
        sql.Identifier(table_name),
        sql.Identifier(which_column),
        sql.Identifier(newname)))


def df_to_gdf(input_df):
    df = input_df.copy()
    geometry = [Point(xy) for xy in zip(df.Longitude_NAD83, df.Latitude_NAD83)]
    return gpd.GeoDataFrame(df, crs="+init=epsg:4326", geometry=geometry)

def csv_to_geojson(input_fp, output_fp):
    csv_data = pd.read_csv(input_fp,
                       sep=',',
                       encoding='utf-8', low_memory=False)
    geojson_data = (csv_data.pipe(df_to_gdf).to_json())
    with open(output_fp, 'w') as geojson_file:
        geojson_file.write(geojson_data)


def indicator_tables(params=None):
    """
    Takes either 'spe' or 'ind' as arguments to create and ingest
    data in geojson format, and sends it to postgis.

    1. selects geojson, and processes it with ogr tools
        - could geopandas do this without ogr??
    2.
    """
    from shapely.geometry import Point
    import psycopg2, gdaltools,os, geopandas as gpd
    from tools import geoconfig, column_name_changer
    path = os.environ['DC_DATA']
    cur = db.str.cursor()
    gdaltools.Wrapper.BASEPATH = 'C:\\OSGeo4W64\\bin'

    which = None
    choice = {'spe':"geoSpe.geojson",
    'ind':'geoInd.geojson'}
    if params is not None:
        if params == 'spe':

            # create schema + ingest
            conf = geoconfig()
            ogr = gdaltools.ogr2ogr()
            which = choice.get('spe')
            ogr.set_encoding("UTF-8")
            ogr.set_input(os.path.join(path,which),srs="EPSG:4326")
            ogr.geom_type = 'POINT'
            con = gdaltools.PgConnectionString(**conf)
            ogr.set_output(con, table_name="geospe")
            ogr.execute()
            print(which+' table with geometry created. \n')

            fname= os.path.join(path,choice[f'{params}'])
            print('reading gpd for colcheck..')
            print(fname)
            df = pd.read_csv(os.path.join(path,'geoSpecies_2.csv'), low_memory=False, nrows=0)

            tbl='geospe'

            try:
                for col in df.columns:
                    if (col.lower()=='longitude_nad84') or (col.lower()=="latitude_nad83"):
                        pass
                    elif matcher(tbl,f'{col}') == col:
                        column_name_changer(tbl,matcher(tbl,f'{col}'), col.upper())
                        db.str.commit()
                        column_name_changer(tbl,col.upper(), col)
                        db.str.commit()
                    else:
                        column_name_changer(tbl,matcher(tbl,f'{col}'), col)
                        db.str.commit()

                        print('Column names fixed.')

            except Exception as e:
                con = db.str
                cur = db.str.cursor()
                con.rollback()
                print(e)

            # db.str.commit()
            cur.execute("""
            ALTER TABLE gisdb.public.geospe
            RENAME TO "geoSpeciesInventory";""")

            # # referencing header
            cur.execute("""
            ALTER TABLE gisdb.public."geoSpeciesInventory"
            ADD CONSTRAINT "geoSpe_PrimaryKey_fkey"
            FOREIGN KEY ("PrimaryKey")
            REFERENCES "dataHeader" ("PrimaryKey");""")
            cur.execute("""
            ALTER TABLE gisdb.public."geoSpeciesInventory"
            ADD COLUMN "DateLoadedInDb" DATE""")
            cur.execute("""
            UPDATE gisdb.public."geoSpeciesInventory"
            SET "DateLoadedInDb"=now()""")
            cur.execute("""
            ALTER TABLE gisdb.public."geoSpeciesInventory"
            DROP COLUMN IF EXISTS "id" """)
            cur.execute("""
            ALTER TABLE gisdb.public."geoSpeciesInventory"
            ADD COLUMN "Public" BOOLEAN""")
            db.str.commit()
            print('geoSpeciesInventory table references header')


        elif params == 'ind':
            conf = geoconfig()
            ogr = gdaltools.ogr2ogr()
            which = choice.get('ind')
            ogr.set_encoding("UTF-8")
            ogr.set_input(os.path.join(path,which),srs="EPSG:4326")
            ogr.geom_type = 'POINT'
            con = gdaltools.PgConnectionString(**conf)
            ogr.set_output(con, table_name="geoind")
            print(which + ' table with geometry created. \n')
            ogr.execute()

            fname= os.path.join(path,choice[f'{params}'])
            print('reading gpd for colcheck..')
            print(fname)
            df = pd.read_csv(os.path.join(path,'geoInd_2.csv'), low_memory=False, nrows=0)

            tbl='geoind'

            try:
                for col in df.columns:
                    if (col.lower()=='longitude_nad84') or (col.lower()=="latitude_nad83"):
                        pass
                    elif matcher(tbl,f'{col}') == col:
                        column_name_changer(tbl,matcher(tbl,f'{col}'), col.upper())
                        db.str.commit()
                        column_name_changer(tbl,col.upper(), col)
                        db.str.commit()
                    else:
                        column_name_changer(tbl,matcher(tbl,f'{col}'), col)
                        db.str.commit()

                        print('Column names fixed.')

            except Exception as e:
                con = db.str
                cur = db.str.cursor()
                con.rollback()
                print(e)

            # changing name
            cur.execute("""
            ALTER TABLE gisdb.public.geoind
            RENAME TO "geoIndicators";""")

            # referencing header
            cur.execute("""
            ALTER TABLE gisdb.public."geoIndicators"
            ADD CONSTRAINT "geoInd_PrimaryKey_fkey"
            FOREIGN KEY ("PrimaryKey")
            REFERENCES "dataHeader" ("PrimaryKey");""")
            # cur.execute("""
            # ALTER TABLE gisdb.public."geoIndicators"
            # ADD COLUMN "DateLoadedInDb" DATE""")
            cur.execute("""
            UPDATE gisdb.public."geoIndicators"
            SET "DateLoadedInDb"=now()""")
            cur.execute("""
            ALTER TABLE gisdb.public."geoIndicators"
            DROP COLUMN IF EXISTS "id" """)
            cur.execute("""
            ALTER TABLE gisdb.public."geoIndicators"
            ADD COLUMN "Public" BOOLEAN""")
            db.str.commit()
            print('geoIndicators table references header')
