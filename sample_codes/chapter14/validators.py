#!/usr/bin/env python
# coding: utf-8

import re

class ValidationError(Exception):
    """
    バリデーションエラー用の例外クラス
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg=msg

    def get_message(self):
        return self.msg


class BaseValidator(object):
    """
    バリデータ用のベースクラス
    """

    def validate(self, value):
        return value


class NotEmpty(BaseValidator):
    """
    項目が空でないことを調べるバリデータ
    """
    errors=(u'この項目は必須です。',)

    def validate(self, value):
        if not value:
            raise ValidationError(self.errors[0])
        return value


class IntValidator(BaseValidator):
    """
    項目が整数の数値であることを調べるバリデータ
    """
    errors=(u'この項目には数値を入力してください。',)

    def validate(self, value):
        try:
            value=int(value)
        except ValueError:
            raise ValidationError(self.errors[0])
        if int(abs(value))!=abs(value):
            raise ValidationError(self.errors[0])
        return value


class IntRangeValidator(BaseValidator):
    """
    値が一定の範囲にあることを調べるバリデータ
    """
    errors=(u'入力された数値が設定された範囲を超えています。',)

    def __init__(self, min_val, max_val):
        self.min=min_val
        self.max=max_val

    def validate(self, value):
        value=IntValidator().validate(value)
        if value>self.max or self.min>value:
            raise ValidationError(self.errors[0])
        return value

class RegexValidator(BaseValidator):
    """
    入力値が正規表現にマッチするかどうか調べるバリデータ
    """
    errors=(u'正しい値を入力してください。',)

    def __init__(self, pat):
        self.regex_pat=re.compile(pat)

    def validate(self, value):
        if not self.regex_pat.search(value):
            raise ValidationError(self.errors[0])
        return value

class URLValidator(RegexValidator):
    """
    URLとして正しい文字列かどうかを調べるバリデータ
    """
    errors=(u'正しいURLを入力してください。',)

    def __init__(self):
        self.regex_pat=re.compile(
            r'^(http|https)://[a-z0-9][a-z0-9\-\._]*\.[a-z]+'
            r'(?:[0-9]+)?(?:/.*)?$', re.I)


class EmailValidator(RegexValidator):
    """
    メールアドレスとして正しい文字列かどうかを調べるバリデータ
    """
    errors=(u'正しいメールアドレスを入力してください。',)

    def __init__(self):
        self.regex_pat=re.compile(
            r'([0-9a-zA-Z_&.+-]+!)*[0-9a-zA-Z_&.+-]+@'
            r'(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+'
            r'[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$')


if __name__=='__main__':
    from unittest import TestCase
    NotEmpty().validate('')
    EmailValidator().validate('hoge@hoge.com')



