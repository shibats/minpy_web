#!/usr/bin/env python
# coding: utf-8
import re

if_pat=re.compile(r"\$if\s+(.*\:)")
endif_pat=re.compile(r"\$endif")
for_pat=re.compile(r"\$for\s+(.*)\s+in\s+(.*\:)")
endfor_pat=re.compile(r"\$endfor")
value_pat=re.compile(r"\${(.+?)}")

class SimpleTemplate(object):
    """
    シンプルな機能を持つテンプレートエンジン
    """

    def __init__(self, body='', file_path=None):
        """
        初期化メソッド
        """
        if file_path:
            f=open(file_path)
            body=unicode(f.read(), 'utf-8', 'ignore')
        body=body.replace('\r\n', '\n')
        self.lines = body.split('\n')
        self.sentences = ((if_pat, self.handle_if),
                          (for_pat, self.handle_for),
                          (value_pat, self.handle_value),)

    def render(self, kws={}):
        """
        テンプレートをレンダリングする
        """
        l, o=self.process(kws=kws)
        return o

    def find_matchline(self, pat, start_line=0):
        """
        正規表現を受け取り，マッチする行の行数を返す
        """
        cur_line=start_line
        for line in self.lines[start_line:]:
            if pat.search(line):
                return cur_line
            cur_line+=1
        return -1

    def process(self, exit_pats=(), start_line=0, kws={}):
        """
        テンプレートのレンダリング処理をする
        """
        output=u''
        cur_line=start_line
        while len(self.lines) > cur_line:
            line=self.lines[cur_line]
            for exit_pat in exit_pats:
                if exit_pat.search(line):
                    return cur_line+1, output
            for pat, handler in self.sentences:
                m=pat.search(line)
                pattern_found=False
                if m:
                    try:
                        cur_line, out=handler(m, cur_line, kws)
                        pattern_found=True
                        output+=out
                        break
                    except Exception, e:
                        raise "Following error occured in line %d\n%s" \
                                            %(cur_line, str(e))
            if not pattern_found:
                output+=line+'\n'
            cur_line+=1
        if exit_pats:
            raise "End of lines while parsing"
        return cur_line, output

    def handle_value(self, _match, _line_no, _kws={}):
        """
        ${...}を処理する
        """
        _line=self.lines[_line_no]
        _rep=[]
        locals().update(_kws)
        pos=0
        while True:
            _m=value_pat.search(_line[pos:])
            if not _m:
                break
            pos+=_m.end()
            _rep.append( (_m.group(1), unicode(eval(_m.group(1)))) )
        for t, r in _rep:
            _line=_line.replace('${%s}'%t, r)
        return _line_no, _line+'\n'

    def handle_if(self, _match, _line_no, _kws={}):
        """
        $ifを処理する
        """
        _cond=_match.group(1)
        if not _cond:
            raise "SyntaxError: invalid syntax in line %d" % line_no
        _cond=_cond[:-1]
        locals().update(_kws)
        _line, _out=self.process((endif_pat, ), _line_no+1, _kws)
        if not eval(_cond):
            _out=''
        return _line-1, _out

    def handle_for(self, _match, _line_no, _kws={}):
        """
        $forを処理する
        """
        _var=_match.group(1)
        _exp=_match.group(2)
        if not _var or not _exp:
            raise "SyntaxError: invalid syntax in line %d" % line_no
        locals().update(_kws)
        _seq=eval(_exp[:-1])
        _out=''
        if not _seq:
            return self.find_matchline(endfor_pat, _line_no), _out
        for _v in _seq:
            _kws.update({_var:_v})
            _line, _single_out=self.process((endfor_pat, ), _line_no+1, _kws)
            _out+=_single_out
        return _line-1, _out


def main():
    t=SimpleTemplate("""aaaa
$if 1==1:
if clause0
$endif

$if 1==1:
if clause1
$if 1==1:
if clause1-2
$endif
$else:
else clause1
$endif

$if 1==1:
if clause2
$endif

$if 1==2:
if clause3
$else:
else clause3
$endif

bbbb
""")
    print t.render()
    print "-"*40

    t=SimpleTemplate("""
<select name="fruit">
$for val in ["Apple", "Banana", "Melon"]:
    <optioin value="${val}">${val}</option>
$endfor
</select>
""")
    print t.render()


if __name__=='__main__':
    """
    import pdb
    pdb.run('main()')
    """
    main()
    