import os.path
import pathlib
import requests
import subprocess
import itertools

import scrapy
from PIL import Image

white = (255, 255, 255)
standard_size = (880, 739)
paste_pos = (0, 610, 880, 739)
background = Image.new('RGBA', standard_size, white)

url = "https://www.nhk.or.jp/lesson/en/letters/hiragana.html"
response = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
if response.status_code != 200:
  raise Exception("Error code: {}. Please check url = {}".format(response.status_code, url))

def download_image(url, code, filename):
  response = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
  if response.status_code != 200:
    raise Exception("Error code: {}. Please check url = {}".format(response.status_code, url))
  with open("db/{:03d}/{}".format(code, filename), "wb") as f:
    f.write(response.content)

url_template = "https://www.nhk.or.jp/lesson/assets/images/letters/{}/{}"
sel = scrapy.selector.Selector(response)
for node in sel.xpath('//div[@class="swiper-slide"]'):
  code = int(node.xpath('div[@class="audio-box"]').attrib['data-audio'])
  name = os.path.split(node.xpath('figure/img').attrib['src'])[1]

  pathlib.Path("db/{:03d}".format(code)).mkdir(parents=True, exist_ok=True)
  download_image(url_template.format("hira", name), code, "hira_{}".format(name))
  download_image(url_template.format("kana", name), code, "kana_{}".format(name))
  download_image(url_template.format("detail/hira", name), code, "detail_hira_{}".format(name))
  download_image(url_template.format("detail/kana", name), code, "detail_kana_{}".format(name))

  subprocess.run(["ffmpeg", "-loglevel", "fatal", "-i",
                  "https://vod-stream.nhk.jp/lesson/assets/data/hls/{}/index.m3u8".format(code),
                  "db/{:03d}/audio.mp3".format(code)])

  im = Image.open("db/{:03d}/detail_hira_{}".format(code, name)).convert("RGBA")
  for coor in itertools.product(range(im.size[0]), range(im.size[1])):
    if im.getpixel(coor)[0] > 150 and im.getpixel(coor)[1] > 150 and im.getpixel(coor)[2] > 150:
        im.putpixel(coor, white)
  im = Image.alpha_composite(background, im.resize(standard_size))
  im.paste(white, paste_pos)
  im.save("db/{:03d}/test_hira_{}".format(code, name))
  im = Image.open("db/{:03d}/detail_kana_{}".format(code, name)).convert("RGBA")
  for coor in itertools.product(range(im.size[0]), range(im.size[1])):
    if im.getpixel(coor)[0] > 150 and im.getpixel(coor)[1] > 150 and im.getpixel(coor)[2] > 150:
        im.putpixel(coor, white)
  im = Image.alpha_composite(background, im.resize(standard_size))
  im.paste(white, paste_pos)
  im.save("db/{:03d}/test_kana_{}".format(code, name))
  print("{:03d} {}".format(code, name))
