import MeCab
import emoji
import neologdn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB

def getStopWords():
    stopWords = []
    with open("./datasets/Japanese.txt", mode="r", encoding="utf-8") as f:
        for word in f:
            if word != "\n":
                stopWords.append(word.rstrip("\n"))
    print("amount of stopWords = {}".format(len(stopWords)))
    return stopWords

def removeEmoji(text):
    return "".join(ch for ch in text if ch not in emoji.UNICODE_EMOJI)

stopWords = getStopWords()
tagger = MeCab.Tagger("mecabrc")
def extractWords(text):
    text = removeEmoji(text)
    text = neologdn.normalize(text)
    words = []
    analyzedResults = tagger.parse(text).split("\n")
    for result in analyzedResults:
        splittedWord = result.split(",")[0].split("\t")[0]
        if not splittedWord in stopWords:
            words.append(splittedWord)
    return words

# 記事データ読み込み
df = pd.read_json("./datasets/merged_article_titles.json", encoding="utf-8")
print(df.head())

# トレーニングデータ・評価データの準備
X = pd.DataFrame(df["articleTitle"])
Y = pd.DataFrame(df["isTrend"])
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.7, test_size=0.3, random_state=10)

# テキストデータのベクトル化（特徴量の抽出）
# 単語の出現回数
vecCount = CountVectorizer(analyzer=extractWords, min_df=3)
vecCount.fit(X_train["articleTitle"])
# 単語の種類
print("word size: ", len(vecCount.vocabulary_))
# 先頭5件の単語を表示
print("word content: ", dict(list(vecCount.vocabulary_.items())[0:5]))
# トレーニング・評価データをベクトル化
X_train_vec = vecCount.transform(X_train["articleTitle"])
X_test_vec = vecCount.transform(X_test["articleTitle"])
# 先頭5件のベクトル化データを表示
print("先頭5件のベクトル化データを表示")
print(pd.DataFrame(X_train_vec.toarray()[0:5], columns=vecCount.get_feature_names()))

# モデル作成
model = BernoulliNB()
model.fit(X_train_vec, Y_train["isTrend"])

# 評価
print("Train accuracy = %.3f" % model.score(X_train_vec, Y_train))
print("Test accuracy = %.3f" % model.score(X_test_vec, Y_test))

# 予測
# 予測テキストデータ作成
data = np.array([
    "アプリをリリースしてみた",
    "Unityチュートリアル",
    "Gitコマンドメモ"
])
df_data = pd.DataFrame(data, columns=["articleTitle"])
# 予測テキストデータをベクトル化
inputVec = vecCount.transform(df_data["articleTitle"])
# ベクトル化データを表示
print("ベクトル化データを表示")
print(pd.DataFrame(inputVec.toarray(), columns=vecCount.get_feature_names()))
# 予測結果
print("予測結果")
print(model.predict(inputVec))
print("各クラスの分類確率")
print(model.predict_proba(inputVec))