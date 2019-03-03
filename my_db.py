
import psycopg2
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class my_db:
    def __init__(self,name=Null):
        pass

    def connect(self):
        with psycopg2.connect(dbname=dbname, user=n,
                                password='mypassword', host='localhost') as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM airport LIMIT 5')

                for row in cursor:
                    print(row)


username = 'postgres'
psw = 'denekra'
dbname = "eda_db"
table1name = 'table1'
table2name = 'table2'

con = connect(user=username, host = '127.0.0.1', password=psw)
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
cur.execute('CREATE DATABASE ' + dbname)
cur.execute('CREATE TABLE ' + table1name)
cur.close()
con.close()