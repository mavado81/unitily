import xml.dom.minidom
import xml.etree.ElementTree
import os
import re
import shutil

r = re.compile('apk')
f = open('tmp.xml')
i = f.read()
doc = xml.dom.minidom.parseString(i)

for node in doc.getElementsByTagName('item'):
    d = '';
    t = '';
    for childs in node.childNodes:
        if childs.nodeName == 'id':
            for child in childs.childNodes:
                d = child.nodeValue
        if childs.nodeName == 'title':
            for child in childs.childNodes:
                t = child.nodeValue
    for dirname, dirnames, filenames in os.walk('./source'):
        for subdirname in dirnames:
            #print type(unicode(subdirname, 'UTF-8')), type(t)
            if unicode(subdirname,'UTF-8') == t:
                print 'match' + t
                for dirname, dirnames, filenames in os.walk('./source/' + subdirname):
                    for filename in filenames:
                        print 'filename:' + filename
                        filecomponet = filename.split('.')
                        print filecomponet[-1]
                        shutil.move('./source/' + subdirname + '/'  + filename, './target/' +d + '.' + filecomponet[-1])

        #print os.path.join(dirname, subdirname)

    #for filename in filenames:
        #print os.path.join(dirname, filename)

