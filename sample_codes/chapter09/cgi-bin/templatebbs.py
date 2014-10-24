#!/usr/bin/env python
# coding: utf-8

import sqlite3
from string import Template
from os import path
from httphandler import Request, Response, get_htmltemplate
import cgitb; cgitb.enable()

con=sqlite3.connect('./bookmark.dat')
cur=con.cursor()
try:
    cur.execute("""CREATE TABLE bookmark (
                   title text, url text);""")
except:
    pass

req=Request()
f=req.form
value_dic={'message':'', 'title':'', 'url':'','bookmarks':''}

if f.has_key('post'):
    if f.getvalue('title', '') and f.getvalue('url', ''):
        cur.execute("""INSERT INTO bookmark(title, url) VALUES(?, ?)""",
                    (f.getvalue('title', ''), f.getvalue('url', '')))
        con.commit()
    else:
        value_dic['message']=u'タイトルとURLは必須項目です'
        value_dic['title']=f.getvalue('title', '')
        value_dic['url']=f.getvalue('url', '')

listbody=''
cur.execute("SELECT title, url FROM bookmark")
for item in cur.fetchall():
    listbody+="""<dt>%s</dt><dd>%s</dd>\n"""%(item)
listbody="""<ul>\n%s</ul>"""%listbody
value_dic['bookmarks']=listbody

res=Response()
f=open(path.join(path.dirname(__file__), 'bookmarkform.html'))
t=Template(unicode(f.read(), 'utf-8', 'ignore'))
body=t.substitute(value_dic)
res.set_body(body)
print res
