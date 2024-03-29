import os.path
import pathlib
import requests
import subprocess

import scrapy

url = "https://www.nhk.or.jp/lesson/en/letters/hiragana.html"
response = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
if response.status_code != 200:
  raise Exception("Error code: {}. Please check url = {}".format(response.status_code, url))

def download_image(url, code, filename):
  response = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
  if response.status_code != 200:
    raise Exception("Error code: {}. Please check url = {}".format(response.status_code, url))
  with open("db/{}/{}".format(code, filename), "wb") as f:
    f.write(response.content)

url_template = "https://www.nhk.or.jp/lesson/assets/images/letters/{}/{}"
sel = scrapy.selector.Selector(response)
for node in sel.xpath('//div[@class="swiper-slide"]'):
  code = node.xpath('div[@class="audio-box"]').attrib['data-audio']
  name = os.path.split(node.xpath('figure/img').attrib['src'])[1]

  pathlib.Path("db/{}".format(code)).mkdir(parents=True, exist_ok=True)
  download_image(url_template.format("hira", name), code, "hira_{}".format(name))
  download_image(url_template.format("kana", name), code, "kana_{}".format(name))
  download_image(url_template.format("detail/hira", name), code, "detail_hira_{}".format(name))
  download_image(url_template.format("detail/kana", name), code, "detail_kana_{}".format(name))

  # TODO: Need to solve errors when using ffmpeg.
  #       Program can run normally, but I don't know what these errors mean and how to solve them.
  subprocess.run(["ffmpeg", "-i", 
                  "https://vod-stream.nhk.jp/lesson/assets/data/hls/{}/index.m3u8".format(code),
                  "db/{}/audio.mp3".format(code)])
