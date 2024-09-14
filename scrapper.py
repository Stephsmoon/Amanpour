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
	'New York Times':'https://www.nytimes.com', 
	'Fox News':'https://www.foxnews.com', 
	'Washington Post':'https://www.washingtonpost.com',
	'CNN':'https://www.cnn.com', 
	'NBC':'https://www.nbcnews.com',
	'USA Today':'https://www.usatoday.com', 
	'Politico':'https://www.politico.com', 
	'ABC News':'https://abcnews.go.com', 
	'Boston Globe':'https://www.bostonglobe.com', 
	'MSNBC News':'https://www.msnbc.com'
}

# Article Object
class Article:
  def __init__(self, image, headline, content):
    self.image = image
    self.headline = headline
    self.content = content

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
		# webscrape from new york times
		if website == 'New York Times':
			# try grab each headline
			try:
				# empty arrays
				headlines = []
				avoid = ["movies", "games"]
				# access website
				soup = BeautifulSoup(urllib.request.urlopen(url),'html.parser')
				# grabs all tags with story wrapper until reaching duplicate
				stories = soup.find_all('section',class_="story-wrapper")
				# for each story in stories
				for story in stories:
					try: 
						grabUrl = story.find('a')['href']
						# check if it ends in html
						pattern = "|".join(avoid)
						if grabUrl.endswith(".html") and not re.search(pattern, grabUrl) :
							headlines.append(grabUrl)
					except: 
						pass
				print(headlines)
			# except 
			except: 
				pass

				'''
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
	'''

	return stored_content

# Test
extractContent()
