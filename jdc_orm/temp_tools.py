from configparser import ConfigParser

# connection credentials within .ini
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

# tool to loop and bring all table names
class tbl_list():
    # empty class variables that will be defined with the 'all' method
    t_list = [] # <- gets list of names
    seen = None # <- empty set used with the conditional

    def all(self):
        # connecting..
        import psycopg2, re
        from temp_tools import config
        params = config()
        con1 = psycopg2.connect(**params)
        cur1 = con1.cursor()
        # looking up all user-defined tables in db
        cur1.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        table_list = cur1.fetchall()
        # loop to remove repeats and add cleaned up names to class variable list
        for tab in table_list:
            self.seen = set(self.t_list)
            if tab not in self.seen:
                self.seen.add(re.search(r"\(\'(.*?)\'\,\)",str(tab)).group(1))
                self.t_list.append(re.search(r"\(\'(.*?)\'\,\)",str(tab)).group(1))


# function to drop all foreign key constraints
def drop_fk(fk_tbl):
    import psycopg2, re
    from psycopg2 import sql
    from temp_tools import config
    params = config()
    con1 = psycopg2.connect(**params)
    cur1 = con1.cursor()
    # default foreign key names: tablename_referencedColName_fkey
    key_str = "{}_PrimaryKey_fkey".format(str(fk_tbl))
    cur1.execute(
    sql.SQL('ALTER TABLE gisdb.public.{0} DROP CONSTRAINT IF EXISTS {1}').format(sql.Identifier(fk_tbl),sql.Identifier(key_str))
    )
    con1.commit()

# function to drop all tables
def drop_tbl(fk_tbl):
    import psycopg2, re
    from psycopg2 import sql
    from temp_tools import config
    params = config()
    con1 = psycopg2.connect(**params)
    cur1 = con1.cursor()
    cur1.execute(
    sql.SQL('DROP TABLE IF EXISTS gisdb.public.{0}').format(sql.Identifier(fk_tbl))
    )
    con1.commit()

# function to create all tables
def create_tbls():
    import psycopg2
    """ all the tables """
    commands = ("""CREATE TABLE "dataHeader"(
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
        "Source" TEXT);""",

        """CREATE TABLE "dataLPI"(
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
            """,
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
                "UOM" TEXT);
                """,
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
                    "Source" TEXT);
                    """,
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

def tbl_ingest():

    subs = 'm_subset/'
    path = 'C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/'
    c = '.csv'
    s = '_subs'
    str='data'
    files = ['header', 'height','gap','spp','soil','lpi']
    for nm in files:
        import os, psycopg2
        from psycopg2 import sql
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if nm == 'header':
            with open(os.path.join(path,nm+c),'r') as f:
                dual = os.path.join(str+nm.capitalize())
                cur.copy_expert(
                sql.SQL("COPY gisdb.public.{0} FROM STDIN WITH CSV HEADER NULL \'NA\'").format(sql.Identifier(dual)), f)
                conn.commit()

        else:
            # print(os.path.join(path,subs+nm+s+c))
            with open(os.path.join(path,subs+nm+s+c)) as f:
                dual = os.path.join(str+nm.capitalize())
                cur.copy_expert(
                sql.SQL("COPY gisdb.public.{0} FROM STDIN WITH CSV HEADER NULL \'NA\'").format(sql.Identifier(dual)), f)
                conn.commit()
