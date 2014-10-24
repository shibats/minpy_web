#!/usr/bin/env python
# coding: utf-8
import sqlite3

class BaseMapper(object):
    """
    シンプルな機能を持つO/Rマッパーのベースクラス
    """
    rows=()

    connection=sqlite3.connect(':memory:')

    @classmethod
    def setconnection(cls, con):
        cls.connection=con

    @classmethod
    def getconnection(cls):
        return cls.connection

    def __init__(self, **kws):
        """
        クラスを初期化する
        idを引数に渡された場合は，既存データをSELECTして返す
        その他のキーワード引数を渡された場合は，データをDBにInsertする
        """
        if 'id' in kws.keys():
            rownames=[v[0] for v in self.__class__.rows]
            rownamestr=', '.join(rownames)
            cn=self.__class__.__name__
            sql="""SELECT %s FROM %s WHERE id=?"""%(rownamestr, cn)
            cur=self.getconnection().cursor()
            cur.execute(sql, (kws['id'],))
            for rowname, v in zip(rownames, cur.fetchone()):
                setattr(self, rowname, v)
            self.id=kws['id']
            cur.close()
        elif kws:
            self.id=self.insert(**kws)
            rownames=[v[0] for v in self.__class__.rows]
            for k in kws.keys():
                if k in rownames:
                    setattr(self, k, kws[k])

    def __repr__(self):
        """
        オブジェクトの文字列表記を定義
        """
        rep=str(self.__class__.__name__)+':'
        rownames=[v[0] for v in self.__class__.rows]
        rep+=', '.join(["%s=%s"%(x, repr(getattr(self, x))) for x in rownames])
        return "<%s>"%rep

    def update(self):
        """
        データを更新する
        """
        sql="""UPDATE %s SET %s WHERE id=?"""
        rownames=[v[0] for v in self.__class__.rows]
        holders=', '.join(['%s=?'%v for v in rownames])
        sql=sql%(self.__class__.__name__, holders)
        values=[getattr(self, n) for n in rownames]
        values.append(self.id)
        cur=self.getconnection().cursor()
        cur.execute(sql, values)
        self.getconnection().commit()
        cur.close()

    @classmethod
    def insert(cls, **kws):
        """
        データを追加し，IDを返す
        """
        sql="""INSERT INTO %s(%s) VALUES(%s)"""
        rownames=', '.join([v[0] for v in cls.rows])
        holders=', '.join(['?' for v in cls.rows])
        sql=sql%(cls.__name__,rownames, holders)
        values=[kws[v[0]] for v in cls.rows]
        cur=cls.getconnection().cursor()
        cur.execute(sql, values)
        cur.execute("SELECT max(id) FROM %s"%cls.__name__)
        newid=cur.fetchone()[0]
        cls.getconnection().commit()
        cur.close()
        return newid

    where_conditions={
        '_gt':'>', '_lt':'<',
        '_gte':'>=', '_lte':'<=',
        '_like':'LIKE' }

    @classmethod
    def select(cls, **kws):
        """
        テーブルからデータをSELECTする
        """
        order=''
        if "order_by" in kws.keys():
            order=" ORDER BY "+kws['order_by']
            del kws['order_by']
        where=[]
        values=[]
        for key in kws.keys():
            ct='='
            kwkeys=cls.where_conditions.keys()
            for ckey in kwkeys:
                if key.endswith(ckey):
                    ct=cls.where_conditions[ckey]
                    kws[key.replace(ckey, '')]=kws[key]
                    del kws[key]
                    key=key.replace(ckey, '')
                    break
            where.append(' '.join((key, ct, '? ')))
            values.append(kws[key])
        wherestr="AND ".join(where)
        sql="SELECT id FROM "+cls.__name__
        if wherestr:
            sql+=" WHERE "+wherestr
        sql+=order
        cur=cls.getconnection().cursor()
        cur.execute(sql, values)
        for item in cur.fetchall():
            ins= cls(id=item[0])
            yield ins
        cur.close()

    @classmethod
    def createtable(cls, ignore_error=False):
        """
        定義に基づいてテーブルを作る
        """
        sql="""CREATE TABLE %s (
               id INTEGER PRIMARY KEY, %s );"""
        columns=', '.join(["%s %s"%(k, v) for k, v in cls.rows])
        sql=sql%(cls.__name__, columns)
        cur=cls.getconnection().cursor()
        try:
            cur.execute(sql)
        except Exception, e:
            if not ignore_error:
                raise e
        cur.close()
        cls.getconnection().commit()


def main():
    class TestMapper(BaseMapper):
        rows=(('foo', 'int'), ('bar', 'text'))

    TestMapper.createtable(True)
    for i in range(10):
        TestMapper(foo=1, bar='abcde')
    ins= TestMapper(id=10)
    ins.foo+=1
    ins.update()
    print ins.foo, ins.bar
    print [x for x in TestMapper.select()]
    print [x for x in TestMapper.select(foo=1, bar_gte='code')]
    print [x for x in TestMapper.select(bar_lte='code',order_by='foo')]
    d=TestMapper(foo=5, bar='abcdefg')
    print d, d.id
    cur=BaseMapper.connection.cursor()


if __name__=='__main__':
    """
    import pdb
    pdb.run('main()')
    """
    main()
    