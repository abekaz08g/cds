#-*-coding:utf-8-*-
from pymongo import Connection
import MeCab
CANDODB = u'candos'
"""
can-do statements
"""


def getKeyWords(string):
    """
    日本語文字列をMeCab解析して、レマ形のリストを返す
    """
    m = MeCab.Tagger()
    res = m.parse(string.encode('utf-8'))
    #print res
    words = res.decode('utf-8').split('\n')
    if len(words) > 0:
        keyWords = [w.split(u',')[-3] for w in words if len(w.split(u',')) > 2]
    return keyWords


class candoStatement:
    """
    can-do statementオブジェクトを作成するクラス
    """
    def __init__(self):
        self.nothing = ''


class candos:
    """
    can-do statements にアクセスするためのオブジェクトを生成
    """
    def __init__(self, colname):
        """
        can-do statements の集合を格納するためのコレクションcolnameを指定してコネクションを開く
        """
        self.con = Connection('localhost', 27017)
        self.db = self.con[CANDODB]
        self.col = self.db[colname]

    def editDescription(self, desc):
        """
        コレクションの説明を記述。任意。
        """
        self.col.update({u'name': u'description'}, {u'cont': desc}, True)

    def setCandoStatement(self, candoStatement, tags):
        """
        データベースにCAN-DO STATEMENTとタグ，キーワードを保存
        """
        keyWords = getKeyWords(candoStatement)
        selector = {u'candoStatement': candoStatement}
        atsp1 = {u'$each': tags}
        atsp2 = {u'$each': keyWords}
        modif = {u'$addToSet': {u'tags': atsp1, u'keyWords': atsp2}}
        self.col.update(selector, modif, True)

    def deleteCandoStatement(self, candoStatement):
        """
        can-do statementの削除
        """
        self.col.remove({u'candoStatement': candoStatement})

    def getCandoStatement(self, candoStatement):
        """
        can-do 記述文文字列からcan-do記述文オブジェクトを取得
        """
        return self.col.find({u'candoStatement': candoStatement})

    def getCandoStatemantsByTags(self, tags):
        """
        tag の集合からcan-do記述文オブジェクトの集合を取得
        """
        res = self.col.find({u'tags': {u'$all': tags}})
        return [r for r in res]
