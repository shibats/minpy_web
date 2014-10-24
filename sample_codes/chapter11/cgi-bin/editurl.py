#!/usr/bin/env python
# coding: utf-8

from simpletemplate import SimpleTemplate
from rssurl import Rssurl
from os import path
from httphandler import Request, Response
import cgitb; cgitb.enable()

errors={}
value_dic={'errors':errors, 'title':'', 'url':'', 'item_id':'' }

req=Request()
f=req.form

p=path.join(path.dirname(__file__), 'editform.html')

if not f.getvalue('posted'):
    id=f.getvalue('id')
    rss=Rssurl(id=int(id))
    value_dic.update({'title':rss.title, 'url':rss.url, 'item_id':id})
else:
    id=f.getvalue('id')
    title=unicode(f.getvalue('title', ''), 'utf-8', 'ignore')
    url=unicode(f.getvalue('url', ''), 'utf-8', 'ignore')
    value_dic.update({'title':title, 'url':url, 'item_id':id})
    if not title:
        errors['title']=u'タイトルを入力してください'
    if not url.startswith('http://'):
        errors['url']=u'正しいURLを入力してください'
    if not errors:
        rss=Rssurl(id=int(f.getvalue('id')))
        rss.title=f.getvalue('title')
        rss.url=f.getvalue('url')
        rss.update()
        p=path.join(path.dirname(__file__), 'posted.html')
        value_dic['message']=u'RSS取得URLを編集しました'

t=SimpleTemplate(file_path=p)
res=Response()
body=t.render(value_dic)
res.set_body(body)
print res

