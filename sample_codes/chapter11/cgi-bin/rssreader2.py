#!/usr/bin/env python
# coding: utf-8

from simpletemplate import SimpleTemplate
from rssurl import Rssurl
from os import path
from httphandler import Request, Response
from rssparser import parse_rss
import cgitb; cgitb.enable()

rsslist=[]
try:
    for rss in Rssurl.select(order_by='id'):
        rsslist.extend(parse_rss(rss.url))
except:
    pass

res=Response()
p=path.join(path.dirname(__file__), 'rsslist.html')
t=SimpleTemplate(file_path=p)
body=t.render({'rsslist':rsslist[:20]})
res.set_body(body)
print res

