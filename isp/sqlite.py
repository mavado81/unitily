import sqlite3
import os

if __name__ == '__main__':
    curdir = os.getcwd()
    newipwhoisdb = curdir + "\\" + "ipwhoishknew.db"
    oldipwhoisdb = curdir + "\\" + "ipwhoishk.db"
    
    #建立ipwhois数据库并初始化表
    create = os.path.exists(newipwhoisdb)
    if create:
        os.remove(newipwhoisdb)
    newconn = sqlite3.connect(newipwhoisdb)
    newcur = newconn.cursor()
    initdb = "CREATE TABLE IF NOT EXISTS ipwhois(inetnum, netname )"
    newcur.execute(initdb)
    newconn.commit()

    conn = sqlite3.connect(oldipwhoisdb)
    cur = conn.cursor()
    sql = "select * from ipwhois"
    cur.execute(sql)
    res = cur.fetchall()

    for f in res:
        newcur.execute("insert into ipwhois (inetnum, netname) values (?, ?)",
                (f[4], f[5]))

    newconn.commit()
    newconn.close()
    conn.commit()
    conn.close()

