import sqlite3
import random as r
from sqlite3 import Error
import pandas as pd
import names
import math as m
import builddb


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

def updatespeed(_conn, oldspeed, newspeed):
    c = _conn.cursor()
    sql = '''update speed set s_speed = ? where s_speed = ?'''
    c.execute(sql, (newspeed, oldspeed))

    c.execute('''update network set n_speed = ? where n_speed = ?''', (newspeed,oldspeed))
    c.execute('''select co_ispname, n_conname from network, contractsoff where co_conname = n_conname and n_speed=?''', (newspeed,))
    n = c.fetchall()
    for isp in n:
        c.execute('''update network set n_price = ? where n_speed = ? and n_conname = ?''', (builddb.priceOfSpeed(newspeed, isp[0]),newspeed, isp[1]))

def deletedev(_conn, devname):
    c = _conn.cursor()
    c.execute('''select d_address from devices where d_devname = ?''', (devname,))
    addy = c.fetchone()[0]
    c.execute('''delete from devices where d_devname = ?''', (devname,))
    c.execute('''update house set devicecount=devicecount-1 where h_address = ?''', (addy,))

def endcontract(_conn, n_address):
    c = _conn.cursor()
    c.execute('''delete from network where n_address = ?''', (n_address,))
    c.execute('''delete from house where h_address = ?''', (n_address,))
    c.execute('''delete from devices where d_address = ?''', (n_address,))

def deleteisp(_conn ,ispname):
    c = _conn.cursor()
    c.execute('''delete from isp where i_ispname = ?''', (ispname,))
    c.execute('''select co_conname from contractsoff where co_ispname = ?''', (ispname,))
    ispcons = c.fetchall()
    c.execute('''delete from contractsoff where co_ispname = ?''', (ispname,))
    for cons in ispcons:
        c.execute('''delete from network where n_conname = ?''', (cons[0],))
        c.execute('''delete from contractsperloc where cpl_conname = ?''', (cons[0],))

def main():
    database = r"proj.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        #insertisp(conn, 'randomname')
        #updatespeed(conn, 50, 60)
        #deletedev(conn, "Judith's console")
        #endcontract(conn, 'Address___#70707')
        deleteisp(conn, 'Pineapple Inc')

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
