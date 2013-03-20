import xml.dom.minidom
import xml.etree.ElementTree
import re
import urllib2

f = open("tmp.xml")
i = f.read()
doc = xml.dom.minidom.parseString(i)

r = re.compile('detail')

for node in doc.getElementsByTagName("item"):
    d = "";
    t = "";
    p = "";
    u = "";
    for childs in node.childNodes:
        if childs.nodeName == "id":
            for child in childs.childNodes:
                d = child.nodeValue
                print d
        if childs.nodeName == "title":
            for child in childs.childNodes:
                t = child.nodeValue
                print t
        if childs.nodeName == "picture":
            for child in childs.childNodes:
                p = child.nodeValue
                print p
        if childs.nodeName == "data_link":
            for child in childs.childNodes:
                u = child.nodeValue
                url = r.sub('download', u)
                print url
   # c = urllib2.urlopen(p).read()
   # h = open(t + '.png', 'w')
   # print 'open file: ' + t + '.png'
   # h.write(c)
   # h.close()
   # print 'close file: ' + t + '.png'
    c = urllib2.urlopen(url).read()
    h = open(d + '.apk', 'w')
    print 'open file: ' + d + '.apk'
    h.write(c)
    h.close()
    print 'close file: ' + d + '.apk'



