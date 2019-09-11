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
