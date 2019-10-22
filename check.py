from tools import config
import os, psycopg2, pyreadr, pandas as pd
from tkinter.filedialog import askopenfilename
params = config()
con = psycopg2.connect(**params)
cur = con.cursor()


# filename.find("header")!=-1
# df.columns[2] in gap.columns
filename = askopenfilename()
print(filename)
if filename.endswith(".csv"):
    missing=dict()
    extra=dict()
    done_str="Done. Please see extra and missing"
    print("reading csv...")
    df=pd.read_csv(filename,low_memory=False)
    if filename.find('header')!=-1:
        print("found a header file")
        header = pd.read_sql_query('SELECT * FROM gisdb.public."dataHeader" LIMIT 1;', con)
        for col in df.columns:
            if col not in header.columns:
                #missing_list = []
                extra.update({'header':{0}.format(col)})
                print(done_str)
        for col in header.columns:
            if col not in df.columns:
                missing.update({'header':{0}.format(col)})

    elif filename.find('gap')!=-1:
        print("found a gap file")
        gap = pd.read_sql_query('SELECT * FROM gisdb.public."dataGap" LIMIT 1;', con)
        for col in df.columns:
            if col not in gap.columns:
                #missing_list = []
                extra.update({'gap':{0}.format(col)})
                print(done_str)
        for col in gap.columns:
            if col not in df.columns:
                missing.update({'gap':{0}.format(col)})
    elif filename.find('height')!=-1:
        print("found a height file")
        height = pd.read_sql_query('SELECT * FROM gisdb.public."dataHeight" LIMIT 1;', con)
        for col in df.columns:
            if col not in height.columns:
                #missing_list = []
                extra.update({'height':{0}.format(col)})
                print(done_str)
        for col in height.columns:
            if col not in df.columns:
                missing.update({'height':{0}.format(col)})

    elif filename.find('spp')!=-1:
        print("found a spp file")
        spp = pd.read_sql_query('SELECT * FROM gisdb.public."dataSpeciesInventory" LIMIT 1;', con)
        for col in df.columns:
            if col not in spp.columns:
                #missing_list = []
                extra.update({'spp':{0}.format(col)})
                print(done_str)
        for col in spp.columns:
            if col not in df.columns:
                missing.update({'spp':{0}.format(col)})

    elif filename.find('soil')!=-1:
        print("found a soil file")
        soil = pd.read_sql_query('SELECT * FROM gisdb.public."dataSoilStability" LIMIT 1;', con)
        for col in df.columns:
            if col not in soil.columns:
                #missing_list = []
                extra.update({'soil':{0}.format(col)})
                print(done_str)
        for col in soil.columns:
            if col not in df.columns:
                missing.update({'soil':{0}.format(col)})

    elif filename.find('lpi')!=-1:
        print("found a lpi file")
        lpi = pd.read_sql_query('SELECT * FROM gisdb.public."dataLPI" LIMIT 1;', con)
        for col in df.columns:
            if col not in lpi.columns:
                #missing_list = []
                extra.update({'lpi':{0}.format(col)})
                print(done_str)
        for col in lpi.columns:
            if col not in df.columns:
                missing.update({'lpi':{0}.format(col)})


elif filename.endswith(".Rdata"):
    print("reading Rdata...")
    try:
        df=pyreadr.read_r(filename)
        print(df.columns)
    except Exception as e:
        print(e)
        print("too large, change it to csv on R")

elif filename.endswith(".geojson"):
    import geopandas as gpd
    if filename.find('species')!=-1:
        geodf = gpd.read_file(filename)
        try:
            geospe = pd.read_sql_query('SELECT * FROM gisdb.public."geoSpeciesInventory" LIMIT 1;', con)
        except Exception as e:
            print(e)
            
        for col in geodf.columns:
            if col not in geospe.columns:
                #missing_list = []
                extra.update({'geoSpe':{0}.format(col)})
                print(done_str)
        for col in geospe.columns:
            if col not in geodf.columns:
                missing.update({'geospe':{0}.format(col)})


    elif filename.find('indicator')!=-1:
        geodf = gpd.read_file(filename)
        geoind = pd.read_sql_query('SELECT * FROM gisdb.public."geoIndicators" LIMIT 1;', con)
        for col in geodf.columns:
            if col not in geoind.columns:
                #missing_list = []
                extra.update({'geoInd':{0}.format(col)})
                print(done_str)
        for col in geoind.columns:
            if col not in geodf.columns:
                missing.update({'geoInd':{0}.format(col)})
