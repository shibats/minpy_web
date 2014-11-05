#!/usr/bin/env python3

import datetime

#フォーマット文字列の作成
html_body = """
<html><body>
{0.year:d}/{0.month:d}/{0.day:d} {0.hour:d}:{0.minute:d}:{0.second:d}
</body></html>"""

now=datetime.datetime.now()

print("Content-type: text/html\n")
print(html_body.format(now))


