import json
import requests
from os import listdir, makedirs

def download_response(url):
  response = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
  if response.status_code != 200:
    raise Exception("Error code: {}. Please check url = {}".format(response.status_code, url))
  return response

media_folder = "COPY_ALL_MEDIA_FILES_HERE_TO_THE_COLLECTION.MEDIA_FOLDER"
makedirs(media_folder, exist_ok=True)
word_index = 0
sentence_index = 0

f = open("japanese-core.txt", "w", encoding="utf-8")
f.write("#separator:tab\n")
f.write("#html:true\n")
f.write("#notetype column:1\n")
f.write("#deck column:2\n")
f.write("#tags column:5\n")

for i in listdir("db"):
  for j in listdir(f"db/{i}"):
    for k in listdir(f"db/{i}/{j}"):
      with open(f"db/{i}/{j}/{k}", "r", encoding="utf-8") as json_file:
        w = json.load(json_file)

      sentences_front = []
      sentences = w["sentences"]
      for s in sentences:
        ja = s["ja"]
        hrkt = s["hrkt"]
        latn = s["latn"]
        en = s["en"]
        if s["image"]:
          image = s["image"]
          image = f"<img src=\"\"{image}\"\" width=\"\"175\"\">"
        else:
          image = ""

        sound = s["sound"]
        response = download_response(sound)
        with open("{}/japanese-core_sentence-{:05d}.mp3".format(media_folder, sentence_index), "wb") as sound_file:
          sound_file.write(response.content)
        sound = "japanese-core_sentence-{:05d}.mp3".format(sentence_index)
        sentence_index += 1

        sound = f"<tr><td rowspan=\"\"4\"\">[sound:{sound}]</td>"
        ja = f"<td>{ja}</td>"
        image = f"<td rowspan=\"\"4\"\">{image}</td></tr>"
        hrkt = f"<tr><td>［{hrkt}］</td></tr>"
        latn = f"<tr><td>{latn}</td></tr>"
        en = f"<tr><td><details><summary>english</summary>{en}</details></td></tr>"
        sentences_front.append(f"{sound}{ja}{image}{hrkt}{latn}{en}")
      sentences_front = "<table width=\"\"100%\"\" border=\"\"1\"\"><tbody>" + "".join(sentences_front) + "</tbody></table>"

      ja = w["ja"]
      hrkt = w["hrkt"]
      latn = w["latn"]
      en = w["en"]
      pos = w["pos"]

      sound = w["sound"]
      response = download_response(sound)
      with open("{}/japanese-core_word-{:04d}.mp3".format(media_folder, word_index), "wb") as sound_file:
        sound_file.write(response.content)
      sound = "japanese-core_word-{:04d}.mp3".format(word_index)
      word_index += 1

      hint = "".join(["_" if c.isalpha() else c for c in en])
      word_front = f"{ja}<br>［{hrkt}］<br><b>（{pos}）</b>{latn}<br>[sound:{sound}] Hint: {hint}"

      back = f"{en}"
      f.write(f"Basic (type in the answer)\tjapanese-core\t\"{word_front}<br>{sentences_front}<br>{i}: {j}\"\t{back}\t\n")
      print(f"{i}> {j}> {k}")

f.close()
