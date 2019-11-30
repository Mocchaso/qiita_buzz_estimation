from twitter import Twitter, OAuth
import config
import re
import json
import emoji

t = Twitter(auth=OAuth(
    config.ACCESS_TOKEN,
    config.ACCESS_SECRET,
    config.CONSUMER_KEY,
    config.CONSUMER_SECRET
))

# トレンド記事タイトルの収集
trendArticleTitles = []
retrieveCount = 200
totalIdx = 0
qiitaTrendAccount = "qiitapoi"
isFinished = False

def retrieveTweets(screenName, count):
    global totalIdx
    timeLine = t.statuses.user_timeline(screen_name=screenName, count=count)
    maxId = 0
    for tweetsIdx, tweet in enumerate(timeLine):
        maxId = tweet["id"]
        addArticleTitles(tweet)
        totalIdx += 1
    print("Starting additional retrieving...")
    retrieveContinuedTweets(screenName, count, maxId)

def retrieveContinuedTweets(screenName, count, maxId):
    global totalIdx, isFinished
    tmpMaxId = maxId
    while True:
        timeLine = t.statuses.user_timeline(screen_name=screenName, count=count, max_id=tmpMaxId)
        prevMaxId = 0
        for tweetsIdx, tweet in enumerate(timeLine):
            tmpMaxId = tweet["id"]
            addArticleTitles(tweet)
            print("totalIdx = {}, prevMaxId = {}, maxId = {}, title = {}\n".format(totalIdx, prevMaxId, tmpMaxId, trendArticleTitles[totalIdx]["articleTitle"]))
            if prevMaxId == 0 and totalIdx % 200 != 0:
                isFinished = True
                break
            prevMaxId = tmpMaxId
            totalIdx += 1
        if isFinished:
            print("Finished collecting {} qiita_trend_titles.".format(totalIdx))
            break

def addArticleTitles(tweet):
    global trendArticleTitles
    tmpTitle = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "", tweet["text"]) # ツイート内のURLを除去
    tmpTitle = ''.join(s for s in tmpTitle if s not in emoji.UNICODE_EMOJI)
    articleTitle = tmpTitle[:len(tmpTitle)-1] # 末尾の半角スペースを除去
    datum = {"articleTitle": articleTitle}
    trendArticleTitles.append(datum)

retrieveTweets(qiitaTrendAccount, retrieveCount)

# 収集したデータのファイル出力
with open("./datasets/qiita_trend_titles.json", mode="w", encoding="utf-8") as f:
    json.dump(trendArticleTitles, f, indent=4, ensure_ascii=False)
print("Finished saving 'Trend Titles' as .json file.")