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
