#!/usr/bin/env python
# coding: utf-8

import sqlite3
from os import path
from simplemapper import BaseMapper

class Rssurl(BaseMapper):
    rows=(('title', 'text'), ('url', 'text'))

p=path.join(path.dirname(__file__), 'urls.dat')
con=sqlite3.connect(p)
BaseMapper.setconnection(con)

Rssurl.createtable(ignore_error=True)

from validators import NotEmpty, IntValidator, URLValidator
from widgets import Hidden, Text, TextArea, Submit, Reset, Form

editforms=(Text('title', u'タイトル',
            validators=(NotEmpty(),), attrs={'size':40}),
           Text('url', u'RSSのURL',
            validators=(URLValidator(),), attrs={'size':40}),
           Hidden('item_id', u'ID',
            validators=(IntValidator(),) ),
           Submit('submit', u'登録'))

editform=Form(editforms, {'action':'/edit', 'method':'POST'})

addforms=(Text('title', u'タイトル',
            validators=(NotEmpty(),), attrs={'size':40}),
          Text('url', u'RSSのURL',
            validators=(URLValidator(),), attrs={'size':40}),
          Submit('submit', u'登録'))

addform=Form(addforms, {'action':'/add', 'method':'POST'})

