## Python Web Scrapper ##
# scrapes specified news websites

import re
import os
import time 
import json
import urllib
import random
import requests
import selenium.webdriver as webdriver
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urlextract import URLExtract

# Image Extraction
extractor = URLExtract()
# HTML Sessions
session = HTMLSession()
# News Websites
websites = {
	'New York Times':'https://www.nytimes.com', 
	'Fox News':'https://www.foxnews.com', 
	'Washington Post':'https://www.washingtonpost.com',
	'CNN':'https://www.cnn.com', 
	'NBC':'https://www.nbcnews.com',
	'USA Today':'https://www.usatoday.com', 
	'Politico':'https://www.politico.com', 
	'ABC News':'https://abcnews.go.com', 
	'Boston Globe':'https://www.bostonglobe.com', 
	'MSNBC News':'https://www.msnbc.com'}

# Article Object
class Article:
	def __init__(self, headline, content, image, link):
		self.headline = headline
		self.content = content
		self.image = image
		self.link = link

# Extraction Function
def extractContent():
	# dictionary which stores article objects
	stored_content = {}
	# obtain unused file name for images
	# ? specifically for storing images
	number = 0
	while os.path.exists(f"image{number}.png"):
		number += 1
	# grabs headlines from each website
	for website, url in websites.items():
		# array which will store Article Objects
		storage = []
		# webscrape from new york times
		if website == 'New York Times':
			# try grab each headline
			try:
				# articles to avoid
				avoid = ["nyregion", "upshot", "opinion", "movies", "fashion", "games", "arts"]
				# access website
				soup = BeautifulSoup(urllib.request.urlopen(url),'html.parser')
				# grabs all tags with story wrapper until reaching duplicate
				stories = soup.find_all('section',class_="story-wrapper")
				# for each story in stories
				for story in stories:
					try: 
						grabUrl = story.find('a')['href']
						# check if article is valid
						if not grabUrl.endswith(".html") or re.search("|".join(avoid), grabUrl):
							continue
						# grab all content
						headline = story.find('p', class_='indicate-hover').text
						# check whether this has any associated text and add it 
						try: 
							content = story.find('p', class_='summary-class').text
						except: 
							pass
						img = 0
						# append object
						storage.append(Article(headline,content,img,grabUrl))
					except Exception as e: 
						print(e) 
						pass
			except Exception as e: 
				print(e) 
				pass
			# add new york times articles
			stored_content[website] = storage
	return stored_content
