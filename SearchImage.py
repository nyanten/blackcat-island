import requests
import shutil

API_PATH    = "https://www.googleapis.com/customsearch/v1"
PARAMS = {
  "cx" : "016355067320953861016:qdj_jc1hz8q", #検索エンジンID
  "key": "AIzaSyB6y17mN6af9ZfLeDAr7P3Eg3q8rgzSUFY", #APIキー
  "q"  : "黒島結菜", #検索ワード
  "searchType": "image", #検索タイプ
  "start" : 1, #開始インデックス
  "num" : 5   #1回の検索における取得件数(デフォルトで10件)
}
LOOP = 2
image_idx = 0

for x in range(LOOP):
  PARAMS.update({'start': PARAMS["num"] * x + 1})
  items_json = requests.get(API_PATH, PARAMS).json()["items"]
  for item_json in items_json:
    path = "images/" + str(image_idx) + ".png"
    r = requests.get(item_json['link'], stream=True)
    if r.status_code == 200:
      with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
      image_idx+=1
