import json
import requests
import config

# Qiita記事一覧の取得先URL
url = "https://qiita.com/api/v2/items"
# アクセストークン認証用のヘッダ
headers = {"Authorization": "Bearer {}".format(config.QIITA_ACCESS_TOKEN)}
# バズった記事かどうかの水準（いいね数の閾値）
notBuzzThreshold = 10
# 1ページ当たりの記事数
per_page = 100

# バズっていない記事のタイトルを収集
articleTitles = []
idx = 0
print("Starting collecting article titles...")
for page in range(3, 101):
    # スパムアカウントによる記事を除外するため、序盤のページは除外
    params = {"page": str(page), "per_page": str(per_page)}
    response = requests.get(url, headers=headers, params=params)
    resJson = response.json()
    for article in resJson:
        if article.get("likes_count") < notBuzzThreshold:
            title = article.get("title")
            articleTitles.append({"articleTitle": title})
            print("{}th article title = {}, url = {}".format(idx, title, article["url"]))
            idx += 1
print("Finished collecting {} qiita_article_titles.".format(idx))

# 収集したデータのファイルを出力
with open("./datasets/qiita_article_titles.json", mode="w", encoding="utf-8") as f:
    json.dump(articleTitles, f, indent=4, ensure_ascii=False)
print("Finished saving 'Trend Titles' as .json file.")