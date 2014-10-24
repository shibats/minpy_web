#!/usr/bin/env python
# coding: utf-8

from simpleappserver import expose, test
from httphandler import Response
from simpletemplate import SimpleTemplate

from validators import NotEmpty, RegexValidator
from widgets import Text, Submit, Form

editforms=(Text('username', u'ユーザ名',
            validators=(NotEmpty(), RegexValidator(r'[A-Za-z\d]')),),
           Text('password', u'パスワード',
            validators=(NotEmpty(), RegexValidator(r'[A-Za-z\d]')),),
           Submit('submit', u'ログイン'))
loginform=Form(editforms, {'action':'/login', 'method':'POST'})

base_body="""<html><body>%s</body></html>"""

@expose
def login_form(_request, values={}, errors={}):
    body=base_body % ('${form.display(values, errors)}')
    res=Response()
    t=SimpleTemplate(body)
    values['password']=''
    body=t.render({'form':loginform, 'values':values, 'errors':errors})
    res.set_body(body)
    return res

from Cookie import SimpleCookie
import md5

fixeduser='user'
fixedpass='pass'

@expose
def login(_request, username='', password=''):
    res=Response()
    values, errors=loginform.validate({'username':username,
                                       'password':password})
    if errors or fixeduser!=username or fixedpass!=password:
        return login_form(_request, values, errors)

    c=SimpleCookie()
    m=md5.md5(username+':'+password)
    c['authhash']=m.hexdigest()
    c['authhash']['expires']='Thu, 1-Jan-2030 00:00:00 GMT'
    res.set_header(*c.output().split(': '))
    res.status=302
    res.set_header('Location', '/')
    res.set_body('')
    return res

@expose
def logout(_request):
    body=base_body % ('<p>Logged out</p>')
    res=Response()
    c=SimpleCookie()
    c['authhash']=''
    res.set_header(*c.output().split(': '))
    res.set_body(body)
    return res

class secured_expose(object):
    """
    認証付きのリクエストハンドラ関数を定義するためのデコレータクラス
    """

    def __init__(self, checkfunc, loginpath='/login_form'):
        self.loginpath=loginpath
        self.checkfunc=checkfunc

    def __call__(self, func):
        def wrapper(_request, *args, **kws):
            if self.checkfunc(_request):
                return func(_request=_request, *args, **kws)
            else:
                res=Response()
                res.status=302
                res.set_header('Location', self.loginpath)
                res.set_body('')
                return res
        expose(wrapper, func_name=func.func_name)
        return wrapper

def checklogin(request):
    c=SimpleCookie(request.headers.getheader('Cookie', ''))
    m=md5.md5(fixeduser+':'+fixedpass)
    digest=m.hexdigest()
    if c.has_key('authhash') and c['authhash'].value==digest:
        return True
    else:
        return False

@secured_expose(checkfunc=checklogin)
def index(_request, foo='', d={'counter':0}):
    body=base_body % ('<p>Logged in!</p>')
    res=Response()
    t=SimpleTemplate(body)
    body=t.render(d)
    d['counter']+=1
    res.set_body(body)
    return res

if __name__=='__main__':
    test()

