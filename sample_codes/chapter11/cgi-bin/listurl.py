#!/usr/bin/env python
# coding: utf-8

from simpletemplate import SimpleTemplate
from rssurl import Rssurl
from os import path
from httphandler import Request, Response
import cgitb; cgitb.enable()

value_dic={'rsslist':[x for x in Rssurl.select(order_by='id')]}

res=Response()
p=path.join(path.dirname(__file__), 'urllist.html')
t=SimpleTemplate(file_path=p)
body=t.render(value_dic)
res.set_body(body)
print res

