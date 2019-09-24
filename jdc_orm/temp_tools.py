"""
This script contains functions and class methods to set up the server using
psycopg2. Across the whole script, cur and con are shorthand for cursor and
connection objects respectively.

1. config and geoconfig, parse information inside an ini file to be
used by other functions that connect to the server.

2. class TableList queries the server using the pull_names method and
populates an internal attribute (__names) with the names of all the tables
currently on the server.

2. drop_foreign_keys executes a 'ALTER TABLE..DROP FOREIGN KEY IF EXISTS..'
SQL query. This enables the table to be modified as its constraints have
been dropped.

3. drop_tables executes an 'DROP TABLE IF EXISTS..' SQL query. Requires table
constraints to be dropped.

4. create_tables creates table schemas using a 'CREATE TABLE..' query.

5. table_ingest batch uploads all the csv into pg table schemas using the
copy_expert function.

6. drop_indicator used for the selective dropping of tables. It splits up table
names into two: dataHeader = 'data' + 'Header', so the user chooses by which
string to filter and which position to filter at.

7. column_name_changer changes column names on a chosen table.

8. indicator_tables creates and ingests tables with a geometry field.


"""

from configparser import ConfigParser


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

        import psycopg2, re
        from temp_tools import config
        params = config()
        con = psycopg2.connect(**params)
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
    import psycopg2, re
    from psycopg2 import sql
    from temp_tools import config
    params = config()
    con = psycopg2.connect(**params)
    cur = con.cursor()

    key_str = "{}_PrimaryKey_fkey".format(str(table))
    cur.execute(
        sql.SQL("""ALTER TABLE gisdb.public.{0}
               DROP CONSTRAINT IF EXISTS {1}""").format(
               sql.Identifier(table),
               sql.Identifier(key_str))
    )
    con.commit()


def drop_table(table):
    """
    Drops the table used as an argument executing a
    "DROP TABLE IF EXISTS.." query.
    """
    import psycopg2, re
    from psycopg2 import sql
    from temp_tools import config

    params = config()
    con = psycopg2.connect(**params)
    cur = con1.cursor()
    cur.execute(
        sql.SQL('DROP TABLE IF EXISTS gisdb.public.{0}').format(
                 sql.Identifier(table)
    )
    con.commit()


def create_tbls():
    """
    Opens a connection, loops through a tuple of "CREATE TABLE.." commands
    and closes the connection.
    """
    import psycopg2
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
    "PercentCoveredByEcoSite" NUMERIC);""","""CREATE TABLE "dataGap"(
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
    "Source" TEXT);""",

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
    "Source" TEXT,
    "Density" INT);
    """
    )
    conn = None
    try:
        params = config()
        print('Connecting...')
        conn = psycopg2.connect(**params)
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

def table_ingest():
    """
    Reads csv data and uploads it into appropriate pg table.
    """

    subdir = 'm_subset/'
    path = 'C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/'
    suffix = '.csv'
    subfiles = '_subs'
    prefix='data'
    files = ['header', 'height','gap','spp','soil','LPI']
    for file in files:
        import os, psycopg2
        from psycopg2 import sql
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if file == 'header':
            with open(os.path.join(path,file+suffix),'r') as f:
                camelcase = os.path.join(prefix+file.capitalize())
                print("Ingesting header..")
                cur.copy_expert(
                sql.SQL("""
                COPY gisdb.public.{0}
                FROM STDIN WITH CSV HEADER NULL \'NA\'""").format(
                sql.Identifier(camelcase)), f)
                cur.execute(
                sql.SQL("""
                UPDATE gisdb.public.{0}
                SET "DateLoadedInDb"=now()""").format(
                sql.Identifier(camelcase)) )
                conn.commit()
                print("Header up.")

        elif file == 'spp':
            a = 'species'
            b = 'inventory'
            with open(os.path.join(path,subdir+file+subfiles+suffix),'r') as f:
                file = os.path.join(a.capitalize()+b.capitalize())
                camelcase = os.path.join(prefix+file)
                print("Ingesting species inventory data..")
                cur.copy_expert(
                sql.SQL("""
                COPY gisdb.public.{0}
                FROM STDIN WITH CSV HEADER NULL \'NA\'""").format(
                sql.Identifier(camelcase)), f)
                cur.execute(
                sql.SQL("""
                UPDATE gisdb.public.{0}
                SET "DateLoadedInDb"=now()""").format(
                sql.Identifier(camelcase)) )
                conn.commit()
                print("Species inventory table up.")

        elif file == 'soil':
            a = 'soil'
            b = 'stability'
            with open(os.path.join(path,
            subdir+file+subfiles+suffix),'r') as f:
                file = os.path.join(a.capitalize()+b.capitalize())
                camelcase = os.path.join(prefix+file)
                print("Ingesting soil stability data..")
                cur.copy_expert(
                sql.SQL("""
                COPY gisdb.public.{0}
                FROM STDIN WITH CSV HEADER NULL \'NA\'""").format(
                sql.Identifier(camelcase)), f)
                cur.execute(
                sql.SQL("""
                UPDATE gisdb.public.{0}
                SET "DateLoadedInDb"=now()""").format(
                sql.Identifier(camelcase)) )
                conn.commit()
                print("Soil stability table up.")

        elif file == 'LPI':
            with open(os.path.join(path,
            subdir+file+subfiles+suffix)) as f:
                camelcase = os.path.join(prefix+file.upper())
                print("Ingesting LPI data..")
                cur.copy_expert(
                 sql.SQL("""
                 COPY gisdb.public.{0}
                 FROM STDIN WITH CSV HEADER NULL \'NA\'""").format(
                 sql.Identifier(camelcase)), f)
                cur.execute(
                 sql.SQL("""
                 ALTER TABLE gisdb.public.{0}
                 DROP COLUMN IF EXISTS "DateLoadedInDb"""").format(
                 sql.Identifier(camelcase)))
                cur.execute(
                 sql.SQL("""
                 ALTER TABLE gisdb.public.{0}
                 ADD COLUMN "DateLoadedInDb" DATE""").format(
                 sql.Identifier(camelcase)))
                cur.execute(
                 sql.SQL("""
                 UPDATE gisdb.public.{0}
                 SET "DateLoadedInDb"=now()""").format(
                 sql.Identifier(camelcase)) )
                conn.commit()
                print("LPI table up.")

        else:
            with open(os.path.join(path,
            subdir+file+subfiles+suffix)) as f:
                camelcase = os.path.join(prefix+file.capitalize())
                print("Ingesting height and gap data..")
                cur.copy_expert(
                 sql.SQL("""
                 COPY gisdb.public.{0}
                 FROM STDIN WITH CSV HEADER NULL \'NA\'""").format(
                 sql.Identifier(camelcase)), f)
                cur.execute(
                 sql.SQL("""
                 ALTER TABLE gisdb.public.{0}
                 DROP COLUMN IF EXISTS "DateLoadedInDb"""").format(
                 sql.Identifier(camelcase)))
                cur.execute(
                 sql.SQL("""
                 ALTER TABLE gisdb.public.{0}
                 ADD COLUMN "DateLoadedInDb" DATE""").format(
                 sql.Identifier(camelcase)))
                cur.execute(
                 sql.SQL("""
                 UPDATE gisdb.public.{0}
                 SET "DateLoadedInDb"=now()""").format(
                 sql.Identifier(camelcase)) )
                conn.commit()
                print("Height and Gap tables up.")



def drop_indicator(prefix,string_position):
    """
    Takes as arguments pg table prefix to filter through list of table names,
    and position in the camelcase names. It uses a "DROP TABLE IF EXISTS.."
    query to drop the table filtered through the user-defined string and
    position. Useful for dropping tables with a specific prefix in their
    name.
    """
    import psycopg2, re
    from psycopg2 import sql
    from temp_tools import config
    from temp_tools import TableList
    tlist = TableList()
    tlist.pull_names()
    params = config()

    string = "{}".format(str(prefix))
    for item in tlist._table_list__names:
        if list(filter(None,
         re.split('([a-z]+)(?=[A-Z])|([A-Z][a-z]+)',
         item)))[string_position] == string:
           print(item +' dropped')
           con = psycopg2.connect(**params)
           cur = con1.cursor()
           cur.execute(
           sql.SQL("DROP TABLE IF EXISTS gisdb.public.{};").format(
           sql.Identifier(item))
           )
           con.commit()


def column_name_changer(table_name,which_column,newname):
    """
    Takes table name, column name and new column name to change a column's
    name.
    """
    from psycopg2 import sql
    from temp_tools import config
    import psycopg2
    params = config()
    con1 = psycopg2.connect(**params)
    cur1 = con1.cursor()

    cur1.execute(
        sql.SQL("""
        ALTER TABLE gisdb.public.{0}
        RENAME COLUMN {1} TO {2}""").format(
        sql.Identifier(table_name),
        sql.Identifier(which_column),
        sql.Identifier(newname)))
    con1.commit()


def indicator_tables(params=None):
    """
    Takes either 'spe' or 'ind' as arguments to create and ingest
    data in geojson format, and sends it to postgis.
    """
    import psycopg2, gdaltools,os, geopandas as gpd
    from temp_tools import geoconfig, column_name_changer
    path = "C:\\Users\\kbonefont.JER-PC-CLIMATE4\\Downloads\\AIM_data\\"
    ogr = gdaltools.ogr2ogr()
    gdaltools.Wrapper.BASEPATH = 'C:\\OSGeo4W64\\bin'

    which = None
    choice = {'spe':'species_geojson.geojson',
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
            print(which+' table with geometry created. \n')
            ogr.execute()

            param = config()
            conn = psycopg2.connect(**param)
            cur = conn.cursor()

            # specifying exceptions (complex cases/camelcase)
            fname=os.path.join(path,which)
            df = gpd.read_file(fname)
            for col in df.columns:
                if col.lower() == 'source':
                    pass
                elif col.lower() == 'geometry':
                    pass
                else:
                    name_q("geospe", col.lower(), col)
            print('Column names fixed.')

            # changing name
            cur.execute("""
            ALTER TABLE gisdb.public.geospe
            RENAME TO "geoSpeciesInventory";""")

            # referencing header
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
            conn.commit()
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

            # change column names
            param = config()
            conn = psycopg2.connect(**param)
            cur = conn.cursor()

            # specifying exceptions (complex cases/camelcase)
            fname=os.path.join(path,which)
            df = gpd.read_file(fname)
            for col in df.columns:
                if col.lower() == 'source':
                    pass
                elif col.lower() == 'geometry':
                    pass
                else:
                    name_q("geoind", col.lower(), col)
            print('Column names fixed.')


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
            cur.execute("""
            UPDATE gisdb.public."geoIndicators"
            SET "DateLoadedInDb"=now()""" )
            conn.commit()
            print('geoIndicators table references header')
        else:
            print("requires parameters")
