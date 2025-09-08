import shutil
from os import listdir, makedirs

media_folder = "COPY_ALL_MEDIA_FILES_HERE_TO_THE_COLLECTION.MEDIA_FOLDER"
makedirs(media_folder, exist_ok=True)

f = open("hirakana-alphabet-no-audio.txt", "w", encoding="utf-8")
f.write("#separator:tab\n")
f.write("#html:true\n")
f.write("#notetype column:1\n")
f.write("#deck column:2\n")
f.write("#tags column:5\n")

template_string = "Basic (type in the answer)\thirakana-alphabet-no-audio\t\"{character}<br><img src=\"\"{image}\"\" style=\"\"max-width: 40%; height: auto;\"\">\"\t{label}\t\n"

for code in listdir("db"):
  label_txt = [filename for filename in listdir("db/{}".format(code)) if "label_" in filename][0]
  with open("db/{}/{}".format(code, label_txt), encoding="utf-8") as label_file:
    hira, kana, en = label_file.read().splitlines()
  hira_img = "test_hira_{}.png".format(label_txt[6:-4])
  kana_img = "test_kana_{}.png".format(label_txt[6:-4])
  if label_txt in ["label_he.txt"]:
    f.write(template_string.format(character = hira,
                                   image = hira_img,
                                   label = "hira+kana, {}".format(en)))
    shutil.copy("db/{}/{}".format(code, hira_img), "{}/{}".format(media_folder, hira_img))
    continue
  f.write(template_string.format(character = hira,
                                 image = hira_img,
                                 label = "hira, {}".format(en)))
  f.write(template_string.format(character = kana,
                                 image = kana_img,
                                 label = "kana, {}".format(en)))
  shutil.copy("db/{}/{}".format(code, hira_img), "{}/{}".format(media_folder, hira_img))
  shutil.copy("db/{}/{}".format(code, kana_img), "{}/{}".format(media_folder, kana_img))

f.close()
