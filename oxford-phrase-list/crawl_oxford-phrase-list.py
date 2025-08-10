import requests, bs4
url = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford-phrase-list"
prefix_url = "https://www.oxfordlearnersdictionaries.com"

r = requests.get(url, headers={"User-agent": "Mozilla/5.0"})
soup = bs4.BeautifulSoup(r.text, "html.parser")

f = open("oxford-phrase-list.db", "w", encoding="utf-8")
f.write("index,phrase,belong_to,definition\n")

for index, value in enumerate(soup.select("#wordlistsContentPanel li")):
  # phrase
  phrase = str(value.a.string)
  # belong_to
  belong_to = str(value.div.span.string)
  # definition
  definition = prefix_url + value.a["href"]
  # insert words into db
  f.write("{},{},{},{}\n".format(index,
                                 phrase,
                                 belong_to,
                                 definition))
f.close()
