import requests, bs4
url = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"
prefix_url = "https://www.oxfordlearnersdictionaries.com"

r = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
soup = bs4.BeautifulSoup(r.text, "html.parser")

f = open("oxford3000-5000.db", "w")
f.write("index,word,ox3000,ox5000,pos,belong_to,definition\n")

for index, value in enumerate(soup.select("#wordlistsContentPanel li")):
  # word
  word = str(value.a.string)
  # ox3000
  ox3000 = value.has_attr("data-ox3000")
  # ox5000
  ox5000 = value.has_attr("data-ox5000")
  # pos
  pos = str(value.span.string)
  # belong_to
  try:
    belong_to = str(value.div.span.string)
  except:
    belong_to = ""
  # definition
  definition = prefix_url + value.a["href"]
  if len(value.a["href"]) <= len("/definition/english/"):
    definition = ""
  # insert words into db
  f.write("{},{},{},{},{},{},{}\n".format(index,
                                          word,
                                          ox3000,
                                          ox5000,
                                          pos,
                                          belong_to,
                                          definition))
f.close()
