import sqlite3
from sqlite3 import Error
import pandas as pd

def createTables(_conn):
    print("Create tables")
    try:
        c = _conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS location(
            l_locname varchar(255) not null,
            availisp varchar(255) not null
            )""")
        print('tmade')
        c.execute("""CREATE TABLE IF NOT EXISTS house(
            h_address varchar(255) not null,
            devicecount int not null,
            h_conname varchar(255) not null,
            h_locname varchar(255) not null
            )""")
        print('tmade')
        c.execute("""CREATE TABLE IF NOT EXISTS contractsoff(
            co_ispname varchar(255) not null,
            co_conname varchar(255) not null
            )""")
        c.execute("""CREATE TABLE IF NOT EXISTS ISP(
            i_ispname varchar(255) not null,
            i_contracts int not null 
            )""")
        print('tmade')
        c.execute("""CREATE TABLE IF NOT EXISTS contractsperloc(
            cpl_conname varchar(255) not null,
            cpl_locname varchar(255) not null
            )""")
        print('tmade')
        c.execute("""CREATE TABLE IF NOT EXISTS devices(
            d_devname varchar(255) not null,
            d_devtype varchar(255) not null,
            d_address varchar(255) not null
            )""")
        print('tmade')
        c.execute("""CREATE TABLE IF NOT EXISTS network(
            n_conname varchar(255) not null,
            n_price int not null,
            n_speed int not null,
            n_address varchar(255) not null
            )""")
        print('tmade')
        c.execute("""CREATE TABLE IF NOT EXISTS speed(
            s_speed int not null,
            s_conname varchar(255) not null,
            s_locname varchar(255) not null
            )""")
        print('tmade')
        _conn.commit()
    except Error as e:
        print(e)

def main():
    database = r"proj.sqlite"

    # create a database connection
    conn = sqlite3.connect(database)
    with conn:
        createTables(conn)
        #populateTables(conn)

    conn.close()


if __name__ == '__main__':
    main()