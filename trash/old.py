
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




conn.commit()




## table name extraction
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
table_list = cur.fetchall()

t_list = []

###########################
for tab in table_list:
    #regex101.com
    t_list.append(re.search(r"\(\'(.*?)\'\,\)",str(tab)).group(1))
# with t_list full, one could execute an alter table with each

# drop_fk runs opens cursor > replaces argument twice in drop_FK statement
def drop_fk(fk_tbl):
    from psycopg2 import sql
    con1 = psycopg2.connect(dbname="gisdb", user=db_user, password=db_password,
                            port="5432", host=db_host)
    cur1 = con1.cursor()
    # need to define a variable that concatenates with FK names,
    # then add both(tablename, fk name) to alter/drop statement

    key_str = "{}_PrimaryKey_fkey".format(str(fk_tbl))
    cur1.execute(
    sql.SQL('ALTER TABLE gisdb.public.{0} DROP CONSTRAINT IF EXISTS {1}').format(sql.Identifier(fk_tbl),sql.Identifier(key_str))
    )
    con1.commit()

def drop_tbl(fk_tbl):
    from psycopg2 import sql
    con1 = psycopg2.connect(dbname="gisdb", user=db_user, password=db_password,
                            port="5432", host=db_host)
    cur1 = con1.cursor()
    cur1.execute(
    sql.SQL('DROP TABLE IF EXISTS gisdb.public.{0}').format(sql.Identifier(fk_tbl))
    )
    con1.commit()

for nm in files:
    import os, psycopg2
    from psycopg2 import sql
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    # load csv: construct csv inside with open
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



import os
a = 'species'
b = 'inventory'
ab = os.path.join(a+b)
print(os.path.join(a.capitalize()+b.capitalize()))
a = 'soil'
b = 'stability'

os.path.join(a.capitalize(),b.capitalize())
c = 'lpi'

subs = 'm_subset/'
path = 'C:/Users/kbonefont.JER-PC-CLIMATE4/Downloads/AIM_data/'
c = '.csv'
s = '_subs'
str='data'
files = ['header', 'height','gap','spp','soil','lpi']

os.path.join(path,subs+str+files[-2]+s+c)


y = [x for x in files if x!='lpi'and x!='spp'and x!='soil']
type(y)

from temp_tools import t_list
tlist = t_list()
