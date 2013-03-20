import xml.dom.minidom
import xml.etree.ElementTree
import re 
import urllib2

f = open('tmp.xml')
i = f.read()
doc = xml.dom.minidom.parseString(i)

for node in doc.getElementsByTagName("item"):
    d = '';
    p = '';
    u = '';
    for childs in node.childNodes:
        if childs.nodeName == 'id':
            for child in childs.childNodes:
                d = child.nodeValue
                print d
        if childs.nodeName == 'picture':
            for child in childs.childNodes:
                p = child.nodeValue
                print p
        if childs.nodeName =='data_link':
            for child in childs.childNodes:
                u = child.nodeValue
                print u
    
    c = urllib2.urlopen(u).read()
    print c
    x = xml.dom.minidom.parseString(c)
    print x
    c = '';

    name = '';
    for node in x.getElementsByTagName('picture'):
        for child in node.childNodes:
            print child.nodeValue
            name = child.nodeValue
            name = name.split('/')
            print name[-1]
            child.nodeValue = '../public/apk/' + name[-1] +'.png'
            print child.nodeValue

    for node in x.getElementsByTagName('download_link'):
        for child in node.childNodes:
            print child.nodeValue
            child.nodeValue = '../public/apk/' + name[-1] + '.apk'
            print child.nodeValue

    h = open('./xml/' + d + '.xml', 'w')
    print 'open file: xml/' + d + '.xml'
    h.write(x.toxml('UTF-8'))
    h.close()
    print 'close file'

