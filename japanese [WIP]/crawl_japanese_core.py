import os
import json
import urllib
import pathlib
import requests

import scrapy
import user_agent

ua = user_agent.generate_user_agent()
def download_response(url):
  response = requests.get(url, headers={"User-agent": ua})
  if response.status_code != 200:
    raise Exception("Error code: {}. Please check url = {}".format(response.status_code, url))
  return response
def download_content(url):
  return download_response(url).content
def download_json(url):
  return json.loads(download_content(url))

# Master Hiragana and Katakana
api = "https://iknow.jp/api/v2/goals/{}"
content_hira = download_json(api.format(24666))
content_kana = download_json(api.format(24667))

pathlib.Path("master_hira_kana").mkdir(parents=True, exist_ok=True)
with open("master_hira_kana/db.csv", "w") as f:
  f.write("index|hira|kana|en|pos|sound|audio|image_hira|image_kana|detail_hira|detail_kana\n")
  for index, (item_hira, item_kana) in enumerate(zip(content_hira["goal_items"],
                                                     content_kana["goal_items"])):
    hira = item_hira["item"]["cue"]["text"]
    kana = item_kana["item"]["cue"]["text"]
    en = item_hira["item"]["response"]["text"]
    pos = item_hira["item"]["cue"]["part_of_speech"]
    sound_url = item_hira["sound"]
    sound = os.path.split(sound_url)[1]
    response = download_response(sound_url)
    with open("master_hira_kana/{}".format(sound), "wb") as sound_file:
      sound_file.write(response.content)
    # Except for some exceptions
    alter_index = index
    if index > 97:
      alter_index -= 12
    elif index > 91:
      alter_index += 6
    elif index > 82:
      alter_index -= 6
    elif index > 79:
      alter_index += 15
    elif index > 76:
      alter_index -= 3
    elif index > 73:
      alter_index += 18
    # Expect that indices of "master_hira_kana" and "db" are the same
    audio = ""
    image_hira = ""
    image_kana = ""
    detail_hira = ""
    detail_kana = ""
    path = "db/{}".format(alter_index)
    for name in os.listdir(path):
        subpath = os.path.join(path, name)
        if "audio" in name:
            audio = subpath
        if "detail_hira" in name:
            detail_hira = subpath
        elif "hira" in name:
            image_hira = subpath
        if "detail_kana" in name:
            detail_kana = subpath
        elif "kana" in name:
            image_kana = subpath
    f.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(index, hira, kana, en, pos, sound,
                                                        audio, image_hira, image_kana, detail_hira, detail_kana))

# Japanese Core
course_codes = []
url = "https://iknow.jp/content/japanese"
response = download_response(url)
sel = scrapy.selector.Selector(response)
for node in sel.xpath('//a[contains(@title, "Japanese Core") and contains(@href, "courses")]/@href'):
  course_codes.append(node.get().split("/")[-1])

pathlib.Path("japanese_core").mkdir(parents=True, exist_ok=True)
word_file = open("japanese_core/words.csv", "w")
sentence_file = open("japanese_core/sentences.csv", "w")
word_file.write("index|ja|hrkt|latn|en|pos|sound\n")
sentence_file.write("index|word_index|ja|hrkt|latn|en|image|sound\n")
word_index = 0
sentence_index = 0

for course in course_codes:
  content = download_json(api.format(course))
  for w in content["goal_items"]:
    ja = w["item"]["cue"]["text"]
    hrkt = w["item"]["cue"]["transliterations"]["Hrkt"]
    latn = w["item"]["cue"]["transliterations"]["Latn"]
    en = w["item"]["response"]["text"]
    pos = w["item"]["cue"]["part_of_speech"]
    sound_url = w["sound"]
    _, sound_ext = os.path.splitext(urllib.parse.urlparse(sound_url).path)
    response = download_response(sound_url)
    with open("japanese_core/word_{}{}".format(word_index, sound_ext), "wb") as sound_file:
      sound_file.write(response.content)
    word_file.write("{}|{}|{}|{}|{}|{}|word_{}{}\n".format(word_index, ja, hrkt, latn, en, pos,
                                                           word_index, sound_ext))
    for s in w["sentences"]:
      ja = s["cue"]["text"]
      hrkt = s["cue"]["transliterations"]["Hrkt"]
      latn = s["cue"]["transliterations"]["Latn"]
      en = s["response"]["text"]
      image_filename = ""
      if s["image"]:
        image_url = s["image"]
        _, image_ext = os.path.splitext(urllib.parse.urlparse(image_url).path)
        image_filename = "sentence_{}{}".format(sentence_index, image_ext)
        response = download_response(image_url)
        with open("japanese_core/{}".format(image_filename), "wb") as image_file:
          image_file.write(response.content)
      sound_url = s["sound"]
      _, sound_ext = os.path.splitext(urllib.parse.urlparse(sound_url).path)
      response = download_response(sound_url)
      with open("japanese_core/sentence_{}{}".format(sentence_index, sound_ext), "wb") as sound_file:
        sound_file.write(response.content)
      sentence_file.write("{}|{}|{}|{}|{}|{}|{}|sentence_{}{}\n".format(sentence_index, word_index, ja, hrkt, latn, en,
                                                                        image_filename, sentence_index, sound_ext))
      sentence_index += 1
    word_index += 1

word_file.close()
sentence_file.close()
