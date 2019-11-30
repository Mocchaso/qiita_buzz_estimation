import json

trendData = {}
normalData = {}
with open("./datasets/qiita_trend_titles.json", "r", encoding="utf-8") as f:
    trendData = json.load(f)
with open("./datasets/qiita_article_titles.json", "r", encoding="utf-8") as f:
    normalData = json.load(f)

print(len(trendData.keys()))
print(len(normalData.keys()))

idx = 0
mergedData = {}
for k, v in trendData.items():
    mergedData[str(idx)] = {
        "articleTitle": v["articleTitle"],
        "isTrend": 1
    }
    idx += 1
for k, v in normalData.items():
    mergedData[str(idx)] = {
        "articleTitle": v["articleTitle"],
        "isTrend": 0
    }
    idx += 1

with open("./datasets/merged_article_titles.json", mode="w", encoding="utf-8") as f:
    json.dump(mergedData, f, indent=4, ensure_ascii=False)
print("Finished saving 'Merged Article Titles' as .json file.")