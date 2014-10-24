#!/usr/bin/env python
# coding: utf-8

from simpletemplate import SimpleTemplate
from rssurl import Rssurl
from os import path
from httphandler import Request, Response
import cgitb; cgitb.enable()

errors={}
value_dic={'errors':errors, 'title':'', 'url':'', 'item_id':''}

req=Request()
f=req.form

if f.getvalue('posted'):
    title=unicode(f.getvalue('title', ''), 'utf-8', 'ignore')
    url=unicode(f.getvalue('url', ''), 'utf-8', 'ignore')
    value_dic.update({'title':title, 'url':url})
    if not title:
        errors['title']=u'タイトルを入力してください'
    if not url.startswith('http://'):
        errors['url']=u'正しいURLを入力してください'
    if [x for x in Rssurl.select(url=url)]:
        errors['url']=u'このURLは登録済みです'
    if not errors:
        Rssurl(title=title, url=url)
        p=path.join(path.dirname(__file__), 'posted.html')
        value_dic['message']=u'RSS取得URLを追加しました'

res=Response()
p=path.join(path.dirname(__file__), 'addform.html')
t=SimpleTemplate(file_path=p)
body=t.render(value_dic)
res.set_body(body)
print res

