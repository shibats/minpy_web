#!/usr/bin/env python
# coding: utf-8

from simpleappserver import expose, test
from httphandler import Response
from simpletemplate import SimpleTemplate

@expose
def index(_request, d={'counter':0}):
    body="""<html><body><p>${counter}</p></body></html>"""
    res=Response()
    t=SimpleTemplate(body)
    body=t.render(d)
    d['counter']+=1
    res.set_body(body)
    return res

if __name__=='__main__':
    test()
