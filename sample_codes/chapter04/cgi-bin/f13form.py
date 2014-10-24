#!/usr/bin/env python
# coding: utf-8

import cgi
from datetime import datetime

html_body = u"""
<html>
  <head>
    <meta http-equiv="content-type"
          content="text/html;charset=utf-8" />
  </head>
  <body>
  <form method="POST" action="/cgi-bin/find13f.py">
    西暦を選んでください:
    <select name="year">
      %s
    </select>
    <input type="submit" />
  </form>
  %s
  </body>
</html>"""

options=''
content=''

now=datetime.now()
for y in range(now.year-10, now.year+10):
    if y!=now.year:
        select=''
    else:
        select=' selected="selected"'
    options+="<option%s>%d</option>" % (select, y)


form=cgi.FieldStorage()
year_str=form.getvalue('year', '')
if year_str.isdigit():
    year=int(year_str)
    friday13=0
    for month in range(1, 13):
        date=datetime(year, month, 13)
        if date.weekday()==4:
            friday13+=1
            content+=u"%d年%d月13日は金曜日です" % (year, date.month)
            content+=u"<br />"

    if friday13:
        content+=u"%d年には合計%d個の13日の金曜日があります" % (year, friday13)
    else:
        content+=u"%d年には13日の金曜日がありません"

print "Content-type: text/html;charset=utf-8\n"
print html_body % (options, content)
