## Python Web Scrapper ##
# scrapes specified news websites

import re
import os
import time 
import json
import urllib
import requests
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
from urlextract import URLExtract

# Image Extraction
extractor = URLExtract()
# News Websites
websites = {
	'Fox News':'https://www.foxnews.com', 
	'New York Times':'https://www.nytimes.com', 
	'Washington Post':'https://www.washingtonpost.com',
	'CNN':'https://www.cnn.com', 
	'NBC':'https://www.nbcnews.com' 
	'USA Today':'https://www.usatoday.com' 
	'Politico':'https://www.politico.com' 
	'ABC News':'https://abcnews.go.com' 
	'Boston Globe':'https://www.bostonglobe.com' 
	'MSNBC News':'https://www.msnbc.com' 
}

# Article Object
class Article:
  def __init__(self, image, headline, content):
    self.image = image
    self.headline = headline
    self.content = content

# Extraction Function
def extract_content(url):

	# Datastructure which stores Article Ovjects
	# ? Array or Dictionary
	stored_content = []

	# Obtain Unused File Name for Images
	# ? specifically for storing images
	number = 0
	while os.path.exists(f"image{number}.png"):
		number += 1

	# Grabs Content from provided URL
	try:
		images = []
		# Webscrape from Newgrounds
		if website in url: 
			# Accesses Image Website and Pulls Main Image
			soup = BeautifulSoup(urllib.request.urlopen(url), 'html.parser')
			# Grabs Title of Image
			stored_content["title"] = soup.find('h2',itemprop="name").text
			# Grab Images from either Main or Gallery
			if soup.find('div',class_='art-view-gallery'):
				# Extract the list of Images
				imgs = extractor.find_urls(str(soup.find('div',class_='art-view-gallery').find('script',src=None)).replace('\\',''))
				# Remove non Pngs or Jpgs
				imgs = [ x for x in img if re.search('(.png|.jpg)',x)]
			else:
				imgs = [soup.find('div',class_='image').find('img')['src']]
			stored_content["images"] = imgs 
			# Grab Descriptions if they Exist
			try: 
				second = soup.find('div',id="author_comments")
				# Check if Text is Filled
				if not second.text == '':
					stored_content["description"] = second.text
				# Check if Extra Images
				if second.find('img')['data-smartload-src']:
					stored_content["images"].append(second.find('img')['data-smartload-src'])
			except: 
				pass
			# Grab Author Information
			author = soup.find('div',class_='item-user').find('a')['href']
			author = author.replace('https://','').replace('.newgrounds.com','')
			author_pfp = soup.find('div',class_='item-user').find('image')['href']
			stored_content["author"] = author
			stored_content["author_pfp"] = author_pfp
	except Exception as error:
		print('Unable to Extract Content')
		print(error)
		return error
	return stored_content

# Testing 
for website in websites:
	result = extract_content(website)
	print(result)
