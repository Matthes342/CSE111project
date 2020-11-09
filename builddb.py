import sqlite3
import random as r
from sqlite3 import Error
import pandas as pd
import names
import math as m

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
            h_locname varchar(255) not null
            )""") # Changed h_conname to be an int to represent the contract index, change back if necessary h_conname int not null,  deleted - for now
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
            s_locname varchar(255) not null
            )""")
        print('tmade')
        _conn.commit()
    except Error as e:
        print(e)

def dropTables(_conn):
    try:
        sql = "DROP TABLE location"
        _conn.execute(sql)
        sql = "DROP TABLE house"
        _conn.execute(sql)
        sql = "DROP TABLE contractsoff"
        _conn.execute(sql)
        sql = "DROP TABLE ISP"
        _conn.execute(sql)
        sql = "DROP TABLE contractsperloc"
        _conn.execute(sql)
        sql = "DROP TABLE devices"
        _conn.execute(sql)
        sql = "DROP TABLE network"
        _conn.execute(sql)
        sql = "DROP TABLE speed"
        _conn.execute(sql)

        _conn.commit()
    except Error as e:
        print(e)

def populateTables(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate table Warehouse")
    try:
        c = _conn.cursor()
        isps = ['Banana Republic Wireless', 'Bojangles Express', 'Pineapple Inc', 'ATAT Wireless', 'Abar Internet']
        cities = ['Merced', 'Los Angeles', 'San Diego', 'Tokyo', 'Moscow']
        devices = ['laptop', 'pc', 'tablet', 'phone', 'console']
        speeds = [10, 50, 100, 250, 1000]
        contractnames=['A', 'B', 'C']

        sql = "INSERT INTO location VALUES (?, ?)"
        for i in cities:
            num = r.randint(0,2)
            for j in range(3): # 3 ISP's per city
                isp = isps[num + j]
                c.execute(sql, (i, isp))
                print("Inserting: (" + i + ", " + isp + ") into: location")

        sql = "INSERT INTO house VALUES (?, ?, ?)"
        for i in cities:
            for j in range(3): # 3 houses per city
                address = "Address___#" + str(r.randint(0,99999))
                count = r.randint(1,20) # 1-20 devices in a house
                c.execute(sql, (str(address), count, i))
                print("Inserting: (" + address + ", " + str(count) + ", " + i + ") into : house")

        sql = 'insert into contractsoff values (?,?)'
        for i in contractnames:
            for j in isps:
                conname = j + '#' + i
                c.execute(sql, (j, conname))
                print("Inserting: (" + j + ',' + conname + ") into: contractsoffered")
        
        sql = 'INSERT INTO ISP VALUES (?, ?)'
        for i in isps:
            c.execute(sql, (i, 3))
            print("Inserting: (" + i + ', 3) into: ISP')
        
        sql = 'insert into speed values (?,?)'
        for i in speeds:
            test = []
            num = r.randint(1, len(cities)-1)
            j = 0
            while j <= num:
                randcity = r.choice(cities)
                if randcity not in test:
                    test.append(randcity)
                    j += 1
            for city in test:
                c.execute(sql, (i, city))
                print("Inserting: (" + str(i) + ' ' + city +') into: speed')

        sql = 'insert into contractsperloc values (?,?)'
        c.execute('select co_conname from contractsoff')
        contracts = c.fetchall()
        for i in contracts:
            test = []
            num = r.randint(0, len(cities)-1)
            j = 0
            while j <= num:
                randcity = r.choice(cities)
                if randcity not in test:
                    test.append(randcity)
                    j += 1
            for city in test:
                c.execute(sql, (i[0], city))
                print("Inserting: (" + str(i[0]) + ' ' + city +') into: contractsperloc')

        sql = 'insert into devices values (?,?,?)'
        c.execute('select h_address, devicecount from house')
        houses = c.fetchall()
        for house in houses:
            for i in range(house[1]):
                dtype = r.choice(devices)
                devicename = names.get_first_name() + "'s " + dtype
                daddress = house[0]
                c.execute(sql, (devicename, dtype, daddress))
                print("Inserting: (" + devicename + ' ' + dtype +' ' + daddress + ') into: speed')
        _conn.commit()
                    
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def priceOfSpeed(speed):
    return 30 * m.log(speed)

def main():
    database = r"proj.sqlite"

    # create a database connection
    conn = sqlite3.connect(database)
    with conn:
        dropTables(conn)
        createTables(conn)
        populateTables(conn)

    conn.close()


if __name__ == '__main__':
    main()
