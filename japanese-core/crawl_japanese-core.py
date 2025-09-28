import os.path
import pathlib
import json
import requests
import scrapy

def download_response(url):
  response = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
  if response.status_code != 200:
    raise Exception("Error code: {}. Please check url = {}".format(response.status_code, url))
  return response
def download_content(url):
  return download_response(url).content
def download_json(url):
  return json.loads(download_content(url))

url = "https://iknow.jp/content/japanese"
courses = {}
response = download_response(url)
sel = scrapy.selector.Selector(response)
for node in sel.xpath('//a[contains(@title, "Japanese Core") and contains(@href, "courses")]'):
  i, j = node.root.text.split(": ")
  if i not in courses:
    courses[i] = {}
  courses[i][j] = node.root.get("href").split("/")[-1]

api = "https://iknow.jp/api/v2/goals/{}"
for i in courses:
  for j in courses[i]:
    pathlib.Path("db/{}/{}".format(i, j)).mkdir(parents=True, exist_ok=True)
    content = download_json(api.format(courses[i][j]))
    word_index = 0
    for w in content["goal_items"]:
      word = {}
      word["ja"] = w["item"]["cue"]["text"]
      word["hrkt"] = w["item"]["cue"]["transliterations"]["Hrkt"]
      word["latn"] = w["item"]["cue"]["transliterations"]["Latn"]
      word["en"] = w["item"]["response"]["text"]
      word["pos"] = w["item"]["cue"]["part_of_speech"]
      word["sound"] = w["sound"]
      word["sentences"] = []
      for s in w["sentences"]:
        sentence = {}
        sentence["ja"] = s["cue"]["text"]
        sentence["hrkt"] = s["cue"]["transliterations"]["Hrkt"]
        sentence["latn"] = s["cue"]["transliterations"]["Latn"]
        sentence["en"] = s["response"]["text"]
        sentence["image"] = s["image"]
        sentence["sound"] = s["sound"]
        word["sentences"].append(sentence)
      with open("db/{}/{}/{:02d}.json".format(i, j, word_index), "w", encoding="utf-8") as f:
        json.dump(word, f, indent=2, ensure_ascii=False)
      word_index += 1
    print(j)
  print(i)
