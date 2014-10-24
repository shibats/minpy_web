#!/usr/bin/env python
# coding: utf-8

from simpletemplate import SimpleTemplate
from os import path
from httphandler import Request, Response
from widgettest_classes import Profile, form

import cgitb; cgitb.enable()
req=Request()
values={}
[values.update({k:req.form.getvalue(k, '')})
                    for k in req.form.keys()]
cvalues, errors=form.validate(values)
if len(req.form.keys())==0:
    errors={'foo':'bar'}

res=Response()
p=path.join(path.dirname(__file__), 'questionform.html')
t=SimpleTemplate(file_path=p)

post_values={'form':form, 'values':values, 'errors':errors,
             'dataposted':False}
if not errors:
    post_values.update(dataposted=True)
body=t.render(post_values)

res.set_body(body)
print res

