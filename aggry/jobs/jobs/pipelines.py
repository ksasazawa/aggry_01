from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3
import datetime
import os
import time
import re

import numpy as np
import unicodedata
from janome.tokenizer import Tokenizer
from sklearn.cluster import DBSCAN
from scipy.sparse import lil_matrix


class JobsPipeline:
    def __init__(self):
        self.cnt = 0

    # 既存のデータを削除
    def open_spider(self, spider):
        # db.sqlite3と同じディレクトリに移動
        os.chdir('../')
        self.connection = sqlite3.connect('db.sqlite3')
        self.c = self.connection.cursor()
        
        if spider.name == "copro":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社コプロ・エンジニアード'
                                ''')
            
        if spider.name == "conma":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社アーキ・ジャパン'
                                ''')
            
        if spider.name == "kyodo":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '共同エンジニアリング株式会社'
                                ''')

        if spider.name == "sekokannavi":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社ウィルオブ・コンストラクション'
                                ''')

        if spider.name == "oreyume":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社夢真'
                                ''')
            
        self.connection.commit()



    # 勤務地を整形してlabel以外のデータを格納
    def process_item(self, item, spider):
        
        # 市区町村までを取得する関数
        def remove_postal_code(address):
            address = address.replace('　', '').replace(' ', '')
            m = re.search(r'(市|区|町|村|郡)', address[4:])
            murayama = re.search(r'村山市', address)
            # 東村山や武蔵村山への対応
            if murayama:
                index = murayama.start() + 3
                return address[:index]
            # それ以外
            elif m:
                index = m.start() + 5
                return address[:index]
            else:
                return address
        
        # 東京都という文字列を含まないか、市区町村を含まない場合抽出対象から外す。    
        if '東京都' not in item.get('location') or re.search(r'(市|区|町|村|郡)', item.get('location')) is None:
            raise DropItem("This item is not located in Tokyo")
        
        else:
            self.cnt += 1
            print(f"{self.cnt}個めのデータです！！！--------------------------------")
            self.c.execute('''
                                INSERT INTO aggry_app_jobs (title, job, location, mod_location, price, detail, agent, url, data_added)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''',(
                                    item.get('title'),
                                    item.get('job'),
                                    item.get('location'),
                                    remove_postal_code(item.get('location')),
                                    item.get('price'),
                                    item.get('detail'),
                                    item.get('agent'),
                                    item.get('url'),
                                    item.get('data_added'),
                                ))
            self.connection.commit()
            return item



    # クラスタリングしてlabel1を更新
    def close_spider(self, spider):

        # IDのリストとタイトルのリストを作成
        self.c.execute('''
                    SELECT id, title FROM aggry_app_jobs
                        ''')
        result = self.c.fetchall()
        result = [list(r) for r in result] # タプルをリストに変換
        input_strings = []
        input_ids = []
        for r in result:
            r[1] = r[1].strip().replace('/', '').replace('|', '').replace('【ConMa(コンマ)】', '') # 機械学習用にタイトルを整形
            input_strings.append(r[1])
            input_ids.append(r[0])

        # 各文字列をUnicode正規化して、janomeでわかちがきにする
        tokenizer = Tokenizer() # janomeトークナイザーの初期化
        tokenized_strings = []
        for string in input_strings:
            # Unicode正規化
            normalized_string = unicodedata.normalize("NFKC", string)
            # janomeでわかちがきにする
            tokens = tokenizer.tokenize(normalized_string)
            tokenized_strings.append([token.surface for token in tokens])

        # 単語リストを作成
        words = set()
        for string in tokenized_strings:
            for token in string:
                words.add(token)
        word_list = list(words)
        word_list.sort()

        # データ行列を作成
        data_matrix = lil_matrix((len(input_strings), len(word_list)), dtype=np.int32)
        for i, string in enumerate(tokenized_strings):
            for token in string:
                j = word_list.index(token)
                data_matrix[i, j] += 1

        # DBSCANクラスタリングを実行
        dbscan = DBSCAN(eps=1.5, min_samples=2) # ep=1.5~3が良い？。1.5だと150個くらいに分割される。
        dbscan.fit(data_matrix.toarray())

        # ID,タイトル、ラベルを格納したリストを作成
        labeling_list = []
        for i, label in enumerate(dbscan.labels_):
            labeling_list.append([input_ids[i], input_strings[i], label])

        # １レコードずつラベルを入れる
        for l in labeling_list:            
            # プレースホルダーを使ったSQL文を作成する
            sql = "update aggry_app_jobs set label1 = ? where id = ?"
            # プレースホルダーに渡す変数をタプルで指定する
            params = (int(l[2]),l[0])
            # SQL文を実行する
            self.c.execute(sql, params)
            
            self.connection.commit()        
        
        self.connection.close()
        
        
        
        


    