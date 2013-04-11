import sys
import os
import re
import time
import sqlite3
from IPy import IP

if __name__ == '__main__':
    curdir = os.getcwd()
    ipwhoisdb = curdir + "\\" + "ipwhoishk.db"
    conn = sqlite3.connect(ipwhoisdb)
    cur = conn.cursor()
    selectdb = "SELECT * FROM ipwhois"
    cur.execute(selectdb)
    res = cur.fetchall()
    starttime = time.time()

    for f in res:
        inet = IP(f[0]).make_net(f[1])
        if sys.argv[1] in inet:
            print(f[5], ":", f[6])
            break;

