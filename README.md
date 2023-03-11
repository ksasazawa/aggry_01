# 派遣求人特化の2✖️アグリゲーションサイト　Aggry

## 概要
施工管理の派遣求人主要サイトから求人情報をクローリングし、類似求人をグルーピング表示。

## 仕様
下記定期実行
- 既存データ削除
- 対象サイトをクローリング<br>
    - https://www.g-career.net/<br>
    - https://conma.jp/<br>
    - https://www.oreyume.com/
- クローリングデータをDBに保存
- 求人タイトルをわかち書きにし、求人タイトル✖️単語の出現回数の行列を作成
- クラスタリングし、各求人にラベリング


## 技術TipsTips
- デプロイ<br>
Replitを使用
- WEBフレームワーク<br>
Django
- クローリング<br>
scrapy
- 定期実行<br>
APScheduler
- 自然言語処理<br>
unicodedata<br>
janome
- クラスタリング<br>
DBSCAN

