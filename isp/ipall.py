import threading
import queue
import sqlite3
import re
import time
import socket
import os
queue = queue.Queue()
def getip(f,ipinfo=None):
    if ipinfo is None:
        ipinfo = []
    for i in (f):
        if i.find("apnic") > -1 and i.find("ipv4") > -1 and i.find("summary") == -1:
            iplist = i.split("|")
            country = iplist[1]
            if country == 'CN' or country == 'HK':
                ipinfo.append(i)
    return(ipinfo)
def getwhoisinfo(rerules,infostr):
    result = ""
    infore = re.compile(rerules)
    infosh = infore.search(infostr)
    if infosh:
        try:
            result = infosh.group().split(':')[1].strip()
        except IndexError:
            result = result
    return(result)
                                 
def ipwhois(i,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    global failip
    if failip is None:
        failip = []
    iplist = i.split("|")
    ip = iplist[3]
    mask = len(bin(int(iplist[4]))) - 3
    date = iplist[5]
    country = iplist[1]
    status1 = iplist[6]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    #time.sleep(1)
    try:
        s.connect(('whois.apnic.net', 43))
        s.send((ip + '\r\n').encode())
    except:
        failip.append(i)
        #continue
    else:
        
        while True:
            v = s.recv(1024)
            if not v:
                break
            z = v.decode(encoding='utf-8',errors='ignore')
            pp = re.compile(r"inetnum[\s\S]*?source[\s\S].*")
            hh = pp.search(z)
            if hh:
                o = hh.group()
                whoisinfo = str(o).strip()
                inetnum = getwhoisinfo("inetnum.*",whoisinfo)
                netname = getwhoisinfo("netname.*",whoisinfo)
                descr = getwhoisinfo("descr.*",whoisinfo)
                admin_c = getwhoisinfo("admin.*",whoisinfo)
                tech_c = getwhoisinfo("tech.*",whoisinfo)
                mnt_by = getwhoisinfo("mnt.by.*",whoisinfo)
                mnt_lower = getwhoisinfo("mnt.lower.*",whoisinfo)
                mnt_routes = getwhoisinfo("mnt.routes.*",whoisinfo)
                status = getwhoisinfo("status.*",whoisinfo)
                changed = getwhoisinfo("changed.*",whoisinfo)
                source = getwhoisinfo("source.*",whoisinfo)
                cur.execute("insert into ipwhois (ip, mask, date, status1,inetnum, netname, descr, country, admin_c, tech_c, mnt_by, mnt_lower, mnt_routes, changed, status, source) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ip, mask, date, status1, inetnum, netname, descr, country, admin_c, tech_c, mnt_by, mnt_lower, mnt_routes, changed, status, source))
                print(ip + ":" +"add in db")
        s.close()
    conn.commit()
    conn.close()
class MyThreading(threading.Thread):
    def __init__(self, queue,db):
        threading.Thread.__init__(self)
        self.queue = queue
        self.db = db
        
    def run(self):
        global count
        while True:
            host = self.queue.get()
            db = self.db
            ipwhois(host,db)
            count = count + 1
            self.queue.task_done()
            
           

if __name__ == '__main__':
    curdir = os.getcwd()
    ipwhoisdb = curdir + "\\" + "ipwhois.db"
    
    #建立ipwhois数据库并初始化表
    create = os.path.exists(ipwhoisdb)
    if create:
        os.remove(ipwhoisdb)
    conn = sqlite3.connect(ipwhoisdb)
    cur = conn.cursor()
    initdb = "CREATE TABLE IF NOT EXISTS ipwhois(ip, mask, date, status1, inetnum, netname, descr, country, admin_c, tech_c, mnt_by, mnt_lower, mnt_routes, changed, status, source)"
    cur.execute(initdb)
    conn.commit()
    conn.close()
    starttime = time.time()
    failip = []
    apnicfile = open("./delegated-apnic-latest.txt",encoding="utf-8")
    hosts = getip(apnicfile)
    global count
    count = 0
    for i in range(1):
        t = MyThreading(queue,ipwhoisdb)
        t.setDaemon(True)
        t.start()
    for host in hosts:
        queue.put(host)
    queue.join()
    
    
    try:
        for i in failip:
            ipwhois(i,ipwhoisdb)
            print(i)
    except:
        print("no time out ip")
    finally:
        print(count)
        endtime = time.time()
        print("usetime:",(endtime-starttime))

