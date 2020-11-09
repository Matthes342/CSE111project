import sqlite3
from sqlite3 import Error
import pandas as pd


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


def createTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create table")
    try:
        c = _conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS warehouse(
            w_warehousekey decimal(9,0) not null,
            w_name char(100) not null,
            w_capacity decimal(6,0) not null,
            w_suppkey decimal(9,0) not null,
            w_nationkey decimal(2,0) not null
            )""")
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")


def dropTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")
    try:
        c = _conn.cursor()
        c.execute("DROP TABLE warehouse")
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")


def populateTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate table")
    c = _conn.cursor()
    c.execute("""Select s_suppkey, s_name from supplier""")
    supp = c.fetchall()
    df = pd.read_sql_query("""select s_suppkey, n_name, c_nationkey, count(c_nationkey) from supplier, customer, orders, lineitem, part, nation
                            where c_custkey = o_custkey and o_orderkey = l_orderkey and l_suppkey = s_suppkey and l_partkey = p_partkey and c_nationkey = n_nationkey
                            group by s_suppkey, n_nationkey""", _conn)
    df2 = pd.read_sql_query("""select s_suppkey, max(pp)*2 from (select s_suppkey, sum(p_size) as pp from lineitem, part, orders, customer, nation, supplier
                           where l_suppkey = s_suppkey and l_partkey = p_partkey and l_orderkey = o_orderkey and o_custkey = c_custkey and c_nationkey = n_nationkey 
                           group BY n_nationkey, s_suppkey) group by s_suppkey""", _conn)
    df = pd.merge(df, df2, on='s_suppkey')
    df = df.sort_values(by=['s_suppkey', 'count(c_nationkey)'], ascending=(True, False))
    i = 1
    for supname in supp:
        singlesupdf = df[df['s_suppkey'] == supname[0]].head(n=2)
        cap = singlesupdf['max(pp)*2'].max()
        c.execute("""INSERT INTO warehouse
            (w_warehousekey, w_name, w_capacity, w_suppkey, w_nationkey) VALUES (?,?,?,?,?)""",
        (i, supname[1] + '___' + singlesupdf['n_name'].iloc[0], cap, supname[0], int(singlesupdf['c_nationkey'].iloc[0])))
        c.execute("""INSERT INTO warehouse
            (w_warehousekey, w_name, w_capacity, w_suppkey, w_nationkey) VALUES (?,?,?,?,?)""",
        (i+1, supname[1] + '___' + singlesupdf['n_name'].iloc[1], cap, supname[0], int(singlesupdf['c_nationkey'].iloc[1])))
        i = i + 2
    _conn.commit()
    print("++++++++++++++++++++++++++++++++++")


def Q1(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q1")
    c = _conn.cursor()
    c.execute("""Select * from warehouse""")
    f = open('output/1.out', 'w+')
    f.write('{:>10} {:<40} {:>10} {:>10} {:>10}\n'.format('wId', 'wName', 'wCap','sId','nId'))
    for n in c.fetchall():
        f.write('{:>10} {:<40} {:>10} {:>10} {:>10}\n'.format(n[0], n[1], n[2], n[3], n[4]))
    f.close()
    print("++++++++++++++++++++++++++++++++++")


def Q2(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q2")
    c = _conn.cursor()
    c.execute("""select n_name, count(*), sum(w_capacity) from warehouse, nation where w_nationkey = n_nationkey group by n_name 
                order by count(*) desc, sum(w_capacity) desc, n_name asc""")
    f = open('output/2.out', 'w+')
    f.write('{:<40} {:>10} {:>10}\n'.format('nation', 'numW', 'totCap'))
    for n in c.fetchall():
        f.write('{:<40} {:>10} {:>10}\n'.format(n[0], n[1], n[2]))
    f.close()
    print("++++++++++++++++++++++++++++++++++")


def Q3(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q3")
    in3 = open('input/3.in', 'r') 
    lines = in3.readlines() 
    nation = lines[0].strip()
    c = _conn.cursor()
    c.execute("""select s_name, n1.n_name, w_name from supplier, nation n1, nation n2, warehouse
        where w_suppkey = s_suppkey and s_nationkey = n1.n_nationkey and w_nationkey = n2.n_nationkey and n2.n_name =? order by s_name asc""", [nation])
    f = open('output/3.out', 'w+')
    f.write('{:<20} {:<20} {:<20}\n'.format('supplier', 'nation', 'warehouse'))
    for n in c.fetchall():
        f.write('{:<20} {:<20} {:<20}\n'.format(n[0], n[1], n[2]))
    f.close()
    print("++++++++++++++++++++++++++++++++++")


def Q4(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q4")
    in4 = open('input/4.in', 'r') 
    lines = in4.readlines() 
    region = lines[0].strip()
    mins = lines[1].strip()
    c = _conn.cursor()
    c.execute("""Select distinct w_name, w_capacity from warehouse, nation, supplier, region 
        where w_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name=? and w_capacity>=? order by w_capacity desc""", (region, mins))
    f = open('output/4.out', 'w+')
    f.write('{:<40} {:>10}\n'.format('warehouse', 'capacity'))
    for n in c.fetchall():
        f.write('{:<40} {:>10}\n'.format(n[0], n[1]))
    f.close()
    print("++++++++++++++++++++++++++++++++++")


def Q5(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q5")
    in5 = open('input/5.in', 'r') 
    lines = in5.readlines() 
    nation = lines[0].strip()
    c = _conn.cursor()
    #c.execute("""select r_name, IFNULL(sum(w_capacity), 0) from warehouse, region, nation n1, nation n2, supplier
    #    where w_nationkey = n1.n_nationkey and n1.n_regionkey = r_regionkey and w_suppkey = s_suppkey and s_nationkey = n2.n_nationkey and n2.n_name =? 
    #    group by r_name""", [nation])
    #c.execute("""select r_name, IFNULL(sum(w_capacity), 0) from supplier, warehouse, region, nation
    #    where w_nationkey = n_nationkey and n_regionkey = r_regionkey and s_nationkey in (select n_nationkey from nation where n_name =?) 
    #    group by r_name""", [nation])
    f = open('output/5.out', 'w+')
    f.write('{:<30} {:>10}\n'.format('region', 'capacity'))
    for n in c.fetchall():
        f.write('{:<30} {:>10}\n'.format(n[0], n[1]))
    f.close()
    print("++++++++++++++++++++++++++++++++++")


def main():
    database = r"data/tpch.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        dropTable(conn)
        createTable(conn)
        populateTable(conn)

        Q1(conn)
        Q2(conn)
        Q3(conn)
        Q4(conn)
        Q5(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
