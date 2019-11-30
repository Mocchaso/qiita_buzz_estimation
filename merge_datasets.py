import json

trendData = {}
normalData = {}
with open("./datasets/qiita_trend_titles.json", "r", encoding="utf-8") as f:
    trendData = json.load(f)
with open("./datasets/qiita_article_titles.json", "r", encoding="utf-8") as f:
    normalData = json.load(f)

print(len(trendData))
print(len(normalData))

mergedData = []
for datum in trendData:
    mergedData.append({
        "articleTitle": datum["articleTitle"],
        "isTrend": 1
    })
for datum in normalData:
    mergedData.append({
        "articleTitle": datum["articleTitle"],
        "isTrend": 0
    })

with open("./datasets/merged_article_titles.json", mode="w", encoding="utf-8") as f:
    json.dump(mergedData, f, indent=4, ensure_ascii=False)
print("Finished saving 'Merged Article Titles' as .json file.")