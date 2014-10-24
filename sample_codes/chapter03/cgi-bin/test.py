#!/usr/bin/env python

import datetime

html_body = """
<html><body>
%d/%d/%d %d:%d:%d
</body></html>"""

now=datetime.datetime.now()

print "Content-type: text/html\n"
print html_body % (now.year, now.month, now.day, 
                   now.hour, now.minute, now.second)


