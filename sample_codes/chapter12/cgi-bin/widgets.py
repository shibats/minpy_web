#!/usr/bin/env python
# coding: utf-8

from simpletemplate import SimpleTemplate

class BaseWidget(object):
    """
    ウィジェットのベースクラス
    """

    def __init__(self, name, label='', options=None,
                 validators=[], attrs={}):
        self.name=name
        self.label=label
        self.options=options
        self.validators=validators
        self.attrs=" ".join('%s="%s"'%(k, v)
                            for k, v in attrs.items())

    def get_label(self, error):
        body=("""<label for="${name}">${label}\n"""
              """$if error:\n"""
              """<span class="error">${error}</span>\n"""
              """$endif\n"""
              """</label>""")
        t=SimpleTemplate(body)
        return t.render({'name':self.name, 'label':self.label,
                         'error':error})

    def get_form(self, value=None):
        return ''

    def display(self, value=None, error=None):
        return self.get_label(error) + self.get_form(value)

    def validate(self, value):
        from validators import ValidationError
        error=None
        for v in self.validators:
            try:
                value=v.validate(value)
            except ValidationError, e:
                error=e.msg
        return value, error


class Text(BaseWidget):
    """
    テキストフィールド用のウィジェット
    """

    def get_form(self, value=''):
        body=("""<input type="text" name="${name}" value="${value}" """
              """ ${attrs} />""")
        t=SimpleTemplate(body)
        return t.render({'name':self.name, 'value':value,
                         'attrs':self.attrs})


class TextArea(BaseWidget):
    """
    テキストフィールド用のウィジェット
    """

    def get_form(self, value=''):
        body="""<textarea name="${name}" ${attrs}>${value}</textarea>"""
        t=SimpleTemplate(body)
        return t.render({'name':self.name, 'value':value,
                         'attrs':self.attrs})


class Select(BaseWidget):
    """
    メニュー用のウィジェット
    """

    def get_form(self, value=''):
        body=("""<select name="${name}" ${attrs}>\n"""
              """$for v in options:\n"""
              """<option value="${v[0]}"\n"""
              """$if value==v[0]:\n"""
              """ selected \n"""
              """$endif\n"""
              """>${v[1]}</option>\n"""
              """$endfor\n"""
              """</select>\n""")
        t=SimpleTemplate(body)
        return t.render({'name':self.name, 'value':value,
                         'options':self.options,
                         'attrs':self.attrs})


class Radio(BaseWidget):
    """
    ラジオボタン用のウィジェット
    """

    def get_form(self, value=''):
        body=("""$for v in options:\n"""
              """${v[1]} : """
              """<input type="radio" name="${name}" value="${v[0]}"\n"""
              """$if value==v[0]:\n"""
              """ checked \n"""
              """$endif\n"""
              """>\n"""
              """$endfor\n""")
        t=SimpleTemplate(body)
        return t.render({'name':self.name, 'value':value,
                         'options':self.options,
                         'attrs':self.attrs})


class Submit(BaseWidget):
    """
    サブミットボタン用のウィジェット
    """

    def get_label(self, error):
        return ''

    def get_form(self, value=''):
        body=("""<input type="submit" value="${label}" """
              """ ${attrs} />""")
        t=SimpleTemplate(body)
        return t.render({'label':self.label, 'attrs':self.attrs})


class Reset(Submit):
    """
    リセットボタン用のウィジェット
    """

    def get_form(self, value=''):
        body=("""<input type="reset" value="${label}" """
              """ ${attrs} />""")
        t=SimpleTemplate(body)
        return t.render({'label':self.label, 'attrs':self.attrs})


class Form(object):
    """
    ウィジェットを登録するフォーム用クラス
    """

    def __init__(self, forms, attrs={}):
        self.forms=forms
        self.attrs=" ".join('%s="%s"'%(k, v)
                            for k, v in attrs.items())

    def display(self, values={}, errors={}):
        container=''
        for f in self.forms:
            container+=f.display(values.get(f.name, ''),
                                 errors.get(f.name, ''))
            container+="""<br clear="all"/>"""
        body=("""<form ${attrs}>\n"""
              """${container}\n"""
              """</form>\n""")
        t=SimpleTemplate(body)
        return t.render({'attrs':self.attrs, 'container':container})

    def validate(self, invalues):
        errors={}
        values={}
        for f in self.forms:
            value, error=f.validate(invalues.get(f.name, ''))
            values[f.name]=value or ''
            if error:
                errors[f.name]=error
        return values, errors


if __name__ == '__main__':
    t1=Text('name1', 'test text', attrs={'id':'abc', 'class':'foo'})
    t2=Select('name2', 'test select', 
             [str(x) for x in range(10)],
             attrs={'id':'abc', 'class':'foo'})
    t3=Radio('name3', 'test select', 
             [str(x) for x in range(10)],
             attrs={'id':'abc', 'class':'foo'})

    form=Form([t1, t2, t3], attrs={'id':'abc', 'class':'foo'})
    print form.display({'name3':'8'})



