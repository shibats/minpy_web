#!/usr/bin/env python
# coding: utf-8

from xml.etree.ElementTree import ElementTree
from urllib import urlopen

def parse_rss(url):
    """
    RSS 2.0をパースして，辞書のリストを返す
    """
    rss=ElementTree(file=urlopen(url))
    root=rss.getroot()
    rsslist=[]
    # RSS 2.0のitem要素だけを抜き出す
    for item in [ x for x in root.getiterator()
                       if "item" in x.tag]:
        rssdict={}
        for elem in item.getiterator():
            for k in ['link', 'title', 'description', 'author', 'pubDate']:
                if k in elem.tag:
                    rssdict[k]=elem.text
                else:
                    rssdict[k]=rssdict.get(k, "N/A")
        rsslist.append(rssdict)
    return rsslist

if __name__=='__main__':
    rss=parse_rss('http://www.pythonware.com/daily/rss.xml')
    for d in rss:
        print "\n".join(["%s : %s"%(k, i) for k, i in d.items()])

