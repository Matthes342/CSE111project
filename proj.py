import sqlite3
from sqlite3 import Error
import pandas as pd
import random as r


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)
    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertisp(_conn, name):
    c = _conn.cursor()
    contractnames=['A', 'B', 'C']
    speeds = []
    locations = []
    c.execute('''select distinct s_speed from speed''')
    for speed in c.fetchall():
        speeds.append(speed[0])
    c.execute('''select distinct l_locname from location''')
    for location in c.fetchall():
        locations.append(location[0])
    c.execute('insert into ISP values (?,?)', (name, 3))

    sql = "INSERT INTO location VALUES (?, ?)"
    num = r.randint(0,len(locations)-1)
    c.execute(sql, (locations[num], name))
    print("Inserting: (" + locations[num] + ", " + name + ") into: location")

    sql = 'insert into contractsoff values (?,?)'
    for i in contractnames:
        conname = name + '#' + i
        c.execute(sql, (name, conname))
        print("Inserting: (" + name + ',' + conname + ") into: contractsoffered")
    
    sql = 'insert into contractsperloc values (?,?)' #contracts per loc is limited based on availisp (only one contract per city)
    c.execute('select co_conname, co_ispname from contractsoff where co_ispname = ?', [name])
    contracts = c.fetchall()
    for i in contracts:
        availcity = []
        test = []
        c.execute('''select l_locname from location where availisp = ?''', [i[1]])
        for city in c.fetchall():
            availcity.append(city[0])
        if len(availcity) == 0:
            break
        num = r.randint(0, len(availcity))
        j = 0
        while j < num:
            randcity = r.choice(availcity)
            if randcity not in test and randcity in availcity:
                test.append(randcity)
                j += 1
        for city in test:
            c.execute(sql, (i[0], city))
            print("Inserting: (" + str(i[0]) + ' ' + city +') into: contractsperloc')

    #alex part

def updatespeed(conn, oldspeed, newspeed):
    sql


def main():
    database = r"proj.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        insertisp(conn, 'benis') #needs extra var for pricing function

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
