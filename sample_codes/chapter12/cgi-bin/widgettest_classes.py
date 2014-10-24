#!/usr/bin/env python
# coding: utf-8

from os import path
import sqlite3
from simplemapper import BaseMapper

class Profile(BaseMapper):
    rows=(('lastname', 'text'), ('firstname', 'text'),
          ('birthyear', 'int'), ('gender', 'int'),
          ('email', 'text'), ('url', 'text'),
          ('language1', 'text'), ('language2', 'text'),
          ('comment', 'text'))


p=path.join(path.dirname(__file__), 'questionnaire.dat')
con=sqlite3.connect(p)
BaseMapper.setconnection(con)
Profile.createtable(ignore_error=True)

from validators import NotEmpty, IntValidator, IntRangeValidator,\
                      URLValidator, EmailValidator, ValidationError
from widgets import Text, Select, Radio, Submit, Reset, Form

languages=[('', '---')]+[(x, x) for x in ['Perl', 'PHP', 'Python', 'Ruby']]
forms=( Text('lastname', u'名字', validators=(NotEmpty(),)),
        Text('firstname', u'名前', validators=(NotEmpty(),)),
        Select('birthyear', u'生まれた年',
                options=[('0', '---')]+\
                        [(str(x), str(x)) for x in range(1940, 2007)],
                validators=(NotEmpty(), IntRangeValidator(1900, 2007),)),
        Radio('gender', u'性別',
                options=(('1', u'男性'), ('2', u'女性')),
                validators=(IntRangeValidator(1, 2),)),
        Text('email', u'メールアドレス',
                validators=(EmailValidator(),), attrs={'size':'40'}),
        Text('url', u'URL',
                validators=(URLValidator(),), attrs={'size':'40'} ),
        Select('language1', u'一番好きな言語は?',
                options=languages, validators=(NotEmpty(),)),
        Select('language2', u'二番目に好きな言語は?',
                options=languages, validators=(NotEmpty(),)),
        Text('comment', u'一言', attrs={'size':'40'} ),
        Submit('submit', u'登録'), Reset('reset', u'クリア'))
form=Form( forms, {'action':'widgettest.py', 'method':'POST'} )

