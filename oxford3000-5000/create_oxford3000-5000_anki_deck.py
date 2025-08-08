import json
import pandas as pd

with open("custom_oxford3000-5000.note") as f:
  content = json.load(f)
  note = {}
  for record in content:
    s = ""
    s += "<ol>"
    for meaning in record["meanings"]:
      s += "<li>{}</li>".format(meaning["meaning"])
      if len(meaning["examples"]) > 0:
        s += "<ul>"
        for example in meaning["examples"]:
          s += "<li>{}</li>".format(example)
        s += "</ul>"
    s += "</ol>"
    note[str(record["index"])] = s
db = pd.read_csv("oxford3000-5000.db")

f = open("oxford3000-5000.txt", "w", encoding="utf-8")
f.write("#separator:tab\n")
f.write("#html:true\n")
f.write("#notetype column:1\n")
f.write("#deck column:2\n")
f.write("#tags column:5\n")

template_string = "Basic (type in the answer)\toxford3000-5000\t\"Oxford 3000: {ox3000}<br>Oxford 5000: {ox5000}<br>POS: {pos}<br>Belong to: {belong_to}<br><a href=\"\"{definition}\"\">Definition</a><br>{note}\"\t{word}\t\n"
note_string = "<ol><li>This is the first meaning.</li><ul><li>This is the first example of the first meaning.</li><li>This is the second one. To do this, we use Ordered List (1, 2, 3, ...) for meanings, then Increase Indent (in Alignment) and use Unordered List for examples.</li></ul><li>This is the second meaning. To do this, we may use Decrease Indent (in Alignment) first.</li><ul><li>This is the second example of the first meaning.</li><li>This is second one. Sometimes, we need to hide keywords. If we want to do that, for example keyword = {}, we can write keyword = ___.</li></ul></ol>"
for index, row in db.iterrows():
  note_s = note_string.format(row["word"])
  if str(row["index"]) in note:
    note_s = note[str(row["index"])]
  f.write(template_string.format(ox3000 = row["ox3000"],
                                 ox5000 = row["ox5000"],
                                 pos = row["pos"],
                                 belong_to = row["belong_to"],
                                 definition = row["definition"],
                                 note = note_s,
                                 word = row["word"]))

f.close()
