#!/usr/bin/env python
# coding: utf-8

import sqlite3
from httphandler import Request, Response, get_htmltemplate
import cgitb; cgitb.enable()

form_body=u"""
  <form method="POST" action="/cgi-bin/dbpole.py">
    好きな軽量言語は?<br />
    %s
    <input type="submit" />
  </form>"""

radio_parts=u"""
<input type="radio" name="language" value="%s" />%s
<div style="border-left: solid %sem red; ">%s</div>
"""

def incrementvalue(cur, lang_name):
    cur.execute("""SELECT value FROM language_pole
                   WHERE name='%s'""" % lang_name)
    item=None
    for item in cur.fetchall():
        cur.execute("""UPDATE language_pole
           SET value=%d WHERE name='%s'""" % (item[0]+1, lang_name))
    if not item:
        cur.execute("""INSERT INTO language_pole(name, value)
                       VALUES('%s', 1)""" % lang_name)

con=sqlite3.connect('./dbfile.dat')
cur=con.cursor()
try:
    cur.execute("""CREATE TABLE language_pole (
                   name text, value int);""")
except:
    pass

content=""
req=Request()
if req.form.has_key('language'):
    incrementvalue(cur, req.form['language'].value)

lang_dic={}
cur.execute("""SELECT name, value FROM language_pole;""")
for res in cur.fetchall():
    lang_dic[res[0]]=res[1]

for lang in ['Perl', 'PHP', 'Python', 'Ruby']:
    num=lang_dic.get(lang, 0)
    content+=radio_parts%(lang, lang, num, num)

con.commit()

res=Response()
body=form_body%content
res.set_body(get_htmltemplate()%body)
print res
