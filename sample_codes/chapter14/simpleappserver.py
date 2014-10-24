#!/usr/bin/env python
# coding: utf-8

import BaseHTTPServer
import SimpleHTTPServer
import cgi
from httphandler import Response

funcs={}
def expose(func, func_name=''):
    """
    リクエストに反応して呼び出される関数を追加する
    """
    if not func_name:
        func_name=func.func_name
    if func_name=='index':
        func_name=''
    funcs.update({func_name:func})
    return func

class SimpleAppServer(SimpleHTTPServer.SimpleHTTPRequestHandler):

    static_dirs=['/static', ]

    def do_GET(self):
        """GETリクエストを処理する"""
        for sdir in self.static_dirs:
            if self.path.startswith(sdir):
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
                return
        i=self.path.rfind('?')
        if i>=0:
            path, query=self.path[:i], self.path[i+1:]
        else:
            path=self.path
            query=''
        self.handle_query(path, query)

    def do_POST(self):
        """POSTリクエストを処理する"""
        length=self.headers.getheader('content-length')
        try:
            nbytes=int(length)
        except (TypeError, ValueError):
            nbytes=0
        data=self.rfile.read(nbytes)
        self.handle_query(self.path, data)

    def handle_query(self, path, query):
        """
        クエリ付きのGET, POSTリクエストをハンドリングする
        """
        args=[]
        path=path[1:]
        if path.find('/') != -1:
            args=path.split('/')[1:]
            path=path.split('/')[0]
        qdict=cgi.parse_qs(query, keep_blank_values=True)
        for k in qdict.keys():
            if isinstance(qdict[k], list) and len(qdict[k]):
                qdict[k]=unicode(qdict[k][0], 'utf-8', 'ignore')
            else:
                qdict[k]=unicode(qdict[k], 'utf-8', 'ignore')
        if path in funcs.keys():
            qdict.update({'_request':self})
            resp=funcs[path](*args, **qdict)
            self.send_response(resp.status, resp.status_message)
            self.wfile.write(str(resp))
        else:
            self.send_error(404, "No such handler function (%r)" % path)


def test(HandlerClass = SimpleAppServer,
         ServerClass = BaseHTTPServer.HTTPServer):
    SimpleHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
