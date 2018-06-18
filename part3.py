## Full Name: Daniella R. Raz
## Uniqname: drraz
## UMID: 86870313

# these should be the only imports you need
import requests
from bs4 import BeautifulSoup

# write your code here
# usage should be python3 part3.py

base_url = "https://www.michigandaily.com/"
r = requests.get(base_url)

soup = BeautifulSoup(r.text, "lxml")

list_of_article_URLS = []

# retrieving urls of the most read articles, making a list to iterate through
for list_of_most_read in soup.find_all(class_ = "view view-most-read view-id-most_read view-display-id-panel_pane_1 view-dom-id-99658157999dd0ac5aa62c2b284dd266"):
    for a in list_of_most_read.find_all('a', href=True):
        list_of_article_URLS.append(a['href'])

# iterating through list of URLs of most read and accessing the title, and byline of each
for URLs in list_of_article_URLS:
    r2 = requests.get(base_url + URLs)
    soup2 = BeautifulSoup(r2.text, "lxml")

    for titles in soup2.find_all("title"):
        print(titles.text.split("|")[0])

    for bylines in soup2.find_all(class_ = "byline"):
        for names in bylines.find_all(class_ = "link"):
            print("by: ", names.text)
