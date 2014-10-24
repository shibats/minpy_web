#!/usr/bin/env python
# coding: utf-8

from simpleappserver import expose, test
from httphandler import Response
from simpletemplate import SimpleTemplate

htmlbody=u"""<html><body>
<h2>お問い合わせフォーム</h2>
<form>
名前 :<br/>
<input type="text" name="name" value="${name}"/> <br/>
本文 :<br/>
<textarea name="body" cols="40" rows="10">${body}</textarea> <br/>
<input type="submit" name="submit" value="送信" />
</form>
</body></html>"""

@expose
def index(_request, name='', body='', submit=''):
    res=Response()
    t=SimpleTemplate(htmlbody)
    body=t.render({'name':name, 'body':body})
    res.set_body(body)
    return res

if __name__=='__main__':
    test()

