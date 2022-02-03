# `ex_01_conection_to_db.py`

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return conn


def create_connection_in_memory():
   """ create a database connection to a SQLite database """
   conn = None
   try:
       conn = sqlite3.connect(":memory:")
       print(f"Connected, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   finally:
       if conn:
           conn.close()

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

def add_projekt(conn, projekt):
   sql = '''INSERT INTO projects(nazwa, start_date, end_date)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, projekt)
   conn.commit()
   return cur.lastrowid

def add_task(conn, zadanie):
    sql = '''INSERT INTO tasks(projekt_id, nazwa, opis, status, start_date, end_date) VALUES (?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, zadanie)
    conn.commit()
    return cur.lastrowid

def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   return rows

def select_where(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

def dell_all(conn, table):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table}")
    conn.commit()
    print("All deleted")

def dell_where(conn, table, **kwargs):
    qs = []
    values = ()
    for k, v in kwargs.items():
        qs.append(f"{k} = ?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f"DELETE FROM {table} WHERE {q}"
    cur = conn.cursor()
    cur.execute(sql,values)
    conn.commit()
    print("Deleted")


if __name__ == '__main__':

    create_projects_sql = """
    -- projects table
    CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        nazwa text NOT NULL,
        start_date text,
        end_date text
    );
    """

    create_tasks_sql = """
    -- zadanie table
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        projekt_id integer NOT NULL,
        nazwa VARCHAR(250) NOT NULL,
        opis TEXT,
        status VARCHAR(15) NOT NULL,
        start_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (projekt_id) REFERENCES projects (id)
    );
    """
    projekt = ("Zrób angielski", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
    projekt2 = ("Znajdź nową pracę", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
    zadanie = (3, "Określ czego szukasz", "Zdecyduj się na konkretne zajęcie", "otwarte", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
    zadanie2 = (3, "Znajdź odpowiednią firmę", "Zbadaj możliwości", "otwarte", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
    zadanie3 = (1, "Czasowniki", "powtórka", "otwarte", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
    zadanie4 = (1, "Rzeczowniki", "powtórka", "zamknięte", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
    db_file = "database.db"
    conn = create_connection(db_file)
    
    if conn is not None:
#        pr_id = add_projekt(conn, projekt)
#        ta_id = add_task(conn, zadanie4)
        dell_where(conn, "tasks", status="zamknięte")
        print(select_all(conn,"tasks"))
        conn.close()

#        
#        pr_id2 = add_projekt(conn, projekt2)
