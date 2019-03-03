
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
import json

class my_db:
    def __init__(self, dbname, username, password, table1name, table2name):
        self.dbname = dbname
        self.username = username
        self.psw = password
        self.table1name = table1name
        self.table2name = table2name
        self.connect()

    def connect(self):
        def connect():
            self.conn = psycopg2.connect(database=self.dbname, user=self.username, password=self.psw, host='127.0.0.1')

        try:
            connect()
        except:
            # create db if not exist
            with psycopg2.connect(dbname='postgres',user='postgres', host='127.0.0.1',password='denekra') as self.conn:
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                self.cmd("CREATE DATABASE %s  ;" % self.dbname)
            connect()
            self.create_tables()

        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def append_data(self,data):
        """
        append parsed data to db
        :param data:
        """
        def write():
            for d in data:
                id = self.get_from_table("""INSERT INTO %s(date,name,author,ingredients,prep_time,nutrition,bookmark,likes,dislikes)VALUES 
                ('%s','%s','%s','%s','%s','%s','%d','%d','%d') RETURNING id"""%(
                            self.table1name,datetime.datetime.now(),d.get('name'),d.get('author'),d.get('ingredients'),
                            d.get('prep_time'),d.get('nutrition'),int(d.get('bookmark')),int(d.get('like')),int(d.get('dislike'))
                         ))

                id = id[0][0]       # foreign key

                for i,step in enumerate(d.get('steps')):
                    self.cmd("""INSERT INTO %s(table1id,date,receptname,stepnumber,action)VALUES 
                    ('%s','%s','%s','%s','%s')"""%(self.table2name,id,datetime.datetime.now(),d.get('recept_name'),i,step))

        try:
            write()
        except:                         # if table doesn't exists
            self.create_tables()        # create them
            write()                     # write data

        self.close_conn()


    def cmd(self,cmd):
        """
        write sql request
        :param cmd: sql request
        """
        with self.conn.cursor() as cur:
            cur.execute(cmd)


    def get_from_table(self,cmd):
        """
        write sql request and get response
        :param cmd: sql request
        :return: response
        """
        with self.conn.cursor() as cur:
            cur.execute(cmd)
            return cur.fetchall()


    def close_conn(self):
        self.conn.close()

    def create_tables(self):
        self.cmd("""CREATE TABLE IF NOT EXISTS %s (
                id serial PRIMARY KEY,
                date date,
                name varchar,
                author varchar,
                ingredients json,
                prep_time varchar,
                nutrition json, 
                bookmark int,
                likes int,
                dislikes int
            );"""%(self.table1name))
        self.cmd("""CREATE TABLE IF NOT EXISTS %s (
                id serial PRIMARY KEY, 
                table1id INTEGER REFERENCES %s (id), 
                date date,
                receptname varchar,
                stepnumber int,
                action varchar
            );"""%(self.table2name, self.table1name))

