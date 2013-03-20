import xml.dom.minidom
import xml.etree.ElementTree
import re 
import urllib2

f = open('tmp.xml')
i = f.read()
doc = xml.dom.minidom.parseString(i)

for node in doc.getElementsByTagName("item"):
    d = '';
    for childs in node.childNodes:
        if childs.nodeName == 'id':
            for child in childs.childNodes:
                d = child.nodeValue
                print d
        if childs.nodeName == 'picture':
            for child in childs.childNodes:
                child.nodeValue = '../public/apk/' + d + '.png'
                print child.nodeValue
        if childs.nodeName =='data_link':
            for child in childs.childNodes:
                child.nodeValue = '../public/apk/' + d + '.xml'
                print child.nodeValue

h = open('convert.xml', 'w')
print 'open file: convert.xml'
h.write(doc.toxml('UTF-8'))
h.close()
print 'close file'

