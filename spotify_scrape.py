# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 20:57:35 2022

@author: andrew
"""
import requests
from bs4 import BeautifulSoup
import unicodedata
import re

url = "https://ultimateclassicrock.com/progressive-rock-songs/"
url2 = "https://www.popmatters.com/141547-best-25-rock-songs-of-all-time-2496025727.html"
page = requests.get(url)
page2 = requests.get(url2)

soup = BeautifulSoup(page.content, "html.parser",from_encoding='ascii')
soup2 = BeautifulSoup(page2.content, "html.parser",from_encoding='ascii')

pagetext = requests.get(url).text
page2text = requests.get(url2).text

souptext = BeautifulSoup(page.content, "lxml")
souptext2 = BeautifulSoup(page2.content, "lxml")

print(souptext.prettify())

raw_text = souptext.find_all("strong")
raw_results = soup.find_all("strong")

raw2 = souptext2.find_all("span", attrs={'color: #666666; font-size: x-large;'})


#bs.find_all('table', attrs={'border': '1' ,'style':'background-color:White;font-size:10pt;border-collapse:collapse;'})

headers = []
for s in raw_results:
    s_new = s.get_text()
    s_new = unicodedata.normalize("NFKD",s_new)
    headers.append(s_new)

song_results = []
for h in headers:
    strip_song = h.replace("\\"," ")
    ss = str(strip_song)
    print(ss)
    ss = strip_song.replace("\\"," ")
    song_results.append(ss)
    
fresh_songs = []
for song in song_results:
    fresh = re.sub(r'^.*?I', '', song)
    fresh_songs.append(fresh)