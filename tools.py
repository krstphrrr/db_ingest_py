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
        params = config()
        con = db.str
        cur = con.cursor()
        # looking up all user-defined tables in db
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
    print('Foreign keys dropped')
    con.commit()


def drop_table(table):
    """
    Drops the table used as an argument executing a
    "DROP TABLE IF EXISTS.." query.
    """
    import re
    con = db.str
    cur = con.cursor()
    cur.execute(
        sql.SQL('DROP TABLE IF EXISTS gisdb.public.{0}').format(
                 sql.Identifier(table))
    )
    con.commit()


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
    "Source" TEXT,
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
    "State" TEXT,
    "PlotKey" TEXT,
    "Source" TEXT,
    "STATE" TEXT,
    "PLOTKEY" TEXT);""",

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
    "Source" TEXT);""",

    """ CREATE TABLE "dataHeight"(
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
    "Source" TEXT);""",

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
    "source" TEXT,
    "Density" INT,
    "Plotkey" TEXT,
    "Position" TEXT,
    "Veg" TEXT,
    "Line" TEXT,
    "Hydro" TEXT,
    "SoilStabSubSurface" TEXT,
    "Pos" TEXT,
    "Rating" TEXT);
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
    cur.execute(
     sql.SQL("""
     COPY gisdb.public.{0}
     FROM STDIN WITH CSV HEADER NULL \'NA\'""").format(
     sql.Identifier(tablename)), file)

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


def table_ingest():
    """
    Reads csv data and uploads it into appropriate pg table.
    """
    # subdir = 'm_subset/'
    path = os.environ['DC_DATA']
    suffix = '.csv'
    prefix = 'data'

    for file in os.listdir(path):
        if os.path.splitext(file)[1]=='.csv' and file.find('header')!=-1:
            with open(os.path.join(path,file),'r') as f:
                camelcase = os.path.join(prefix+'header'.capitalize())
                print("Ingesting header..")
                queryfun(camelcase, f)
                print("Header up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('spp')!=-1:
            with open(os.path.join(path,file),'r') as f:
                camelcase = os.path.join(prefix+'SpeciesInventory')
                print("Ingesting species inventory..")
                queryfun(camelcase, f)
                print("Species inventory up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('soil')!=-1:
            with open(os.path.join(path,file),'r') as f:
                camelcase = os.path.join(prefix+'SoilStability')
                print("Ingesting soilstability..")
                queryfun(camelcase, f)
                print("soilstability up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('LPI')!=-1:
            with open(os.path.join(path,file),'r') as f:
                camelcase = os.path.join(prefix+'LPI')
                print("Ingesting LPI..")
                queryfun(camelcase, f)
                print("LPI up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('height')!=-1:
            with open(os.path.join(path,file),'r') as f:
                camelcase = os.path.join(prefix+'Height')
                print("Ingesting height..")
                queryfun(camelcase, f)
                print("height up.")

        elif os.path.splitext(file)[1]=='.csv' and file.find('gap')!=-1:
            with open(os.path.join(path,file),'r') as f:
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

class db:
    params = config()
    # str = connect(**params)
    str_1 = SimpleConnectionPool(minconn=1,maxconn=10,**params)
    str = str_1.getconn()

    def __init__(self):

        self._conn = connect(**params)
        self._cur= self._conn.cursor()

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


#
#
#
# import os
# import os.path
# import geopandas as gpd
# path = "C:\\Users\\kbonefont\\Desktop\\data"
# which = "geospehead.geojson"
# fname=os.path.join(path,which)
#
# df = gpd.read_file(fname)
# # #
# indicator_tables('spe')

def indicator_tables(params=None):
    """
    Takes either 'spe' or 'ind' as arguments to create and ingest
    data in geojson format, and sends it to postgis.
    """
    import psycopg2, gdaltools,os, geopandas as gpd
    from tools import geoconfig, column_name_changer
    path = "C:\\Users\\kbonefont\\Desktop\\data"
    ogr = gdaltools.ogr2ogr()
    gdaltools.Wrapper.BASEPATH = 'C:\\OSGeo4W64\\bin'

    which = None
    choice = {'spe':"species_geojson.geojson",
    'ind':'indicators_geojson.geojson'}
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



            # fname= "C:\\Users\\kbonefont\\Desktop\\data\\geospehead.geojson"
            # df = gpd.read_file(fname)

            # tbl='geospe'

            # for col in df.columns:
            #     if col.lower()=='geometry':
            #         pass
            #     elif matcher(tbl,f'{col}') == col:
            #         column_name_changer(tbl,matcher(tbl,f'{col}'), col.upper())
            #         db.str.commit()
            #         column_name_changer(tbl,col.upper(), col)
            #         db.str.commit()
            #     else:
            #         column_name_changer(tbl,matcher(tbl,f'{col}'), col)
            #
            #         print('Column names fixed.')


                # db.str.rollback()

            # db.str.commit()
            # cur.execute("""
            # ALTER TABLE gisdb.public.geospe
            # RENAME TO "geoSpeciesInventory";""")
            #
            # # referencing header
            # cur.execute("""
            # ALTER TABLE gisdb.public."geoSpeciesInventory"
            # ADD CONSTRAINT "geoSpe_PrimaryKey_fkey"
            # FOREIGN KEY ("PrimaryKey")
            # REFERENCES "dataHeader" ("PrimaryKey");""")
            # cur.execute("""
            # ALTER TABLE gisdb.public."geoSpeciesInventory"
            # ADD COLUMN "DateLoadedInDb" DATE""")
            # cur.execute("""
            # UPDATE gisdb.public."geoSpeciesInventory"
            # SET "DateLoadedInDb"=now()""")
            # cur.execute("""
            # ALTER TABLE gisdb.public."geoSpeciesInventory"
            # DROP COLUMN IF EXISTS "id" """)
            # cur.execute("""
            # ALTER TABLE gisdb.public."geoSpeciesInventory"
            # ADD COLUMN "Public" BOOLEAN""")
            # db.str.commit()
            # print('geoSpeciesInventory table references header')






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



# name_check1()
def finishing_queries():
    cur = db.str.cursor()
    cur.execute("""
    ALTER TABLE gisdb.public.geospe
    RENAME TO "geoSpeciesInventory";""")
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


def col_fixer_species(tbl):
    """
    needs db.str, gpd, column_name_changer, matcher
    """
    fname= "C:\\Users\\kbonefont\\Desktop\\data\\geospehead.geojson"
    df = gpd.read_file(fname)
    try:
        for col in df.columns:
            if col.lower()=='geometry':
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
        db.str.rollback()
        print(e)

def name_check2():
    # change column names
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # specifying exceptions (complex cases/camelcase)
    fname=os.path.join(path,which)
    df = gpd.read_file(fname)
    tbl = 'geoind'
    try:
        for col in df.columns:
            if col.lower()=='geometry':
                pass
            elif matcher(tbl,f'{col}') == col:
                column_name_changer(tbl,matcher(tbl,f'{col}'), col.upper())
                conn.commit()
                column_name_changer(tbl,col.upper(), col)
                conn.commit()
            else:
                column_name_changer(tbl,matcher(tbl,f'{col}'), col)
            # column_name_changer("geoind", col.capitalize(), col.lower())
            # column_name_changer("geoind", col.upper(), col)
                print('Column names fixed.')

    except Exception as e:
        conn.rollback()
        print(e)
    conn.commit()
    #
    #
    # # changing name
    # cur.execute("""
    # ALTER TABLE gisdb.public.geoind
    # RENAME TO "geoIndicators";""")
    #
    # # referencing header
    # cur.execute("""
    # ALTER TABLE gisdb.public."geoIndicators"
    # ADD CONSTRAINT "geoInd_PrimaryKey_fkey"
    # FOREIGN KEY ("PrimaryKey")
    # REFERENCES "dataHeader" ("PrimaryKey");""")
    # cur.execute("""
    # UPDATE gisdb.public."geoIndicators"
    # SET "DateLoadedInDb"=now()""" )
    # conn.commit()
    # print('geoIndicators table references header')
