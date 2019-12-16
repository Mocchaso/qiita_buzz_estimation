# kaggleのSMS Spam Collection Datasetでナイーブベイズを体験する
# コード：https://qiita.com/fujin/items/50fe0e0227ef8457a473

import matplotlib.pyplot as pyplot
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB

# -データ準備-
# CSV読み込み
df = pd.read_csv("./datasets/spam.csv", encoding="latin-1")
# 未使用列を削除
df.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1, inplace=True)
# リネーム
df.rename(columns={"v1":"class", "v2":"text"}, inplace=True)
# データの先頭5件を表示
print("データの先頭5件を表示")
print(df.head())

# -トレーニング・評価データ準備-
# トレーニング・評価データを分割
X = pd.DataFrame(df["text"])
Y = pd.DataFrame(df["class"])
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.7, test_size=0.3, random_state=10)

# -テキストデータのベクトル化-
# 単語の出現回数
vecCount = CountVectorizer(min_df=3)
vecCount.fit(X_train["text"])
# 単語の種類
print("word size: ", len(vecCount.vocabulary_))
# 先頭5件の単語を表示
print("word content: ", dict(list(vecCount.vocabulary_.items())[0:5]))
# トレーニング・評価データをベクトル化
X_train_vec = vecCount.transform(X_train["text"])
X_test_vec = vecCount.transform(X_test["text"])
# 先頭5件のベクトル化データを表示
print("先頭5件のベクトル化データを表示")
print(pd.DataFrame(X_train_vec.toarray()[0:5], columns=vecCount.get_feature_names()))

# -モデル作成-
# ベルヌーイモデル
model = BernoulliNB()
model.fit(X_train_vec, Y_train["class"])

# -評価-
print("Train accuracy = %.3f" % model.score(X_train_vec, Y_train))
print("Test accuracy = %.3f" % model.score(X_test_vec, Y_test))

# -予測-
# 予測テキストデータ作成
data = np.array([
    "I am happy.",
    "Are you happy? 00",
    "Free service! Please contact me immediately. But it is 300 US dollars next month."
])
df_data = pd.DataFrame(data, columns=["text"])
# 予測テキストデータをベクトル化
inputVec = vecCount.transform(df_data["text"])
# ベクトル化データを表示
print("ベクトル化データを表示")
print(pd.DataFrame(inputVec.toarray(), columns= vecCount.get_feature_names()))
# 予測結果
print("予測結果")
print(model.predict(inputVec))