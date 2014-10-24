#!/usr/bin/env python
# coding: utf-8

from os import path
from copy import copy
from simpleappserver import expose, test
from httphandler import Response, get_htmltemplate
from simpletemplate import SimpleTemplate

from authentication import secured_expose, relativepath, checklogin

from rssparser import parse_rss
from rssclasses import Rssurl, addform, editform

def get_add_form(values={}, errors={}):
    res=Response()
    t=SimpleTemplate(file_path=relativepath('form.html'))
    body=t.render({'message': u'RSS巡回用URLの追加',
                   'form':addform,
                   'values':values, 'errors':errors})
    res.set_body(body)
    return res

@secured_expose(checkfunc=checklogin)
def add_form(_request, values={}, errors={}):
    return get_add_form(values, errors)

@secured_expose(checkfunc=checklogin)
def add(_request, title='', url=''):
    res=Response()
    values, errors=addform.validate({'title':title, 'url':url})
    if [ x for x in Rssurl.select(url=url)]:
        errors['url']=u'このURLは登録済みです'
    if errors:
        return get_add_form(values, errors)
    Rssurl(title=title, url=url)
    t=SimpleTemplate(file_path=relativepath('posted.html'))
    body=t.render({'message': u'巡回用URLを追加しました'})
    res.set_body(body)
    return res

def get_edit_form(item_id, values={}, errors={}):
    res=Response()
    t=SimpleTemplate(file_path=relativepath('form.html'))
    if not values:
        for item in Rssurl.select(id=item_id):
            pass
        values={'item_id':item_id, 'title':item.title, 'url':item.url}
    body=t.render({'message': u'RSS巡回用URLの編集',
                   'form':editform,
                   'values':values, 'errors':errors})
    res.set_body(body)
    return res

@secured_expose(checkfunc=checklogin)
def edit_form(_request, item_id, values={}, errors={}):
    return get_edit_form(item_id, values, errors)

@secured_expose(checkfunc=checklogin)
def edit(_request, item_id, title='', url=''):
    res=Response()
    values, errors=editform.validate({'item_id':item_id,
                            'title':title, 'url':url})
    if errors:
        return get_edit_form(item_id, values, errors)
    for item in Rssurl.select(id=item_id):
        item.title=title
        item.url=url
    t=SimpleTemplate(file_path=relativepath('posted.html'))
    body=t.render({'message': u'巡回用URLを編集しました'})
    res.set_body(body)
    return res

@secured_expose(checkfunc=checklogin)
def listurl(_request):
    res=Response()
    rsslist=Rssurl.select()
    t=SimpleTemplate(file_path=relativepath('urllist.html'))
    body=t.render({'rsslist': rsslist})
    res.set_body(body)
    return res

@secured_expose(checkfunc=checklogin)
def index(_request):
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
    return res


if __name__=='__main__':
    test()

