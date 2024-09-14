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
	'''try:
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
	return stored_content'''

	if website == 'Fox News':
			# try grab each headline
			try:
				# empty arrays
				headlines = []
				# access website
				soup = BeautifulSoup(urllib.request.urlopen(url),'html.parser')
				# grabs all tags with story wrapper until reaching duplicate
				stories = soup.find_all('h3')
				print(stories)
				counter = 0
				for h3 in stories:
					# gets the titles of each of the news headline
					title_text = h3.get_text(strip=True)
					counter += 1
					# print(title_text)
					# title_pic = h3.find('scr')
					# img_src = img['img']

					# gets the link for each of the headline
					link = h3.find('a')
					# checks for the hyperlink and then prints it
					if link and link.get('href'):
						href = link['href']
						print(f"Title: {title_text}")
						print(f"Link: {href}")
						# print(f"Picture Link: {img_src}")
						print('---')
						print(f"The Number of articles from Fox: {counter}")
				# for each story in stories
				# print(stories)
				
			# except 
			except: 
				pass

	if website == 'Politico':
			# try grab each headline
			try:
				# empty arrays
				politico_headlines = []
				# access website
				politico_soup = BeautifulSoup(urllib.request.urlopen(url),'html.parser')
				# grabs all tags with story wrapper until reaching duplicate
				politico_stories = politico_soup.find_all('h3', class_="headline is-standard-typeface")
				#print(po_stories)
				counter = 0
				for h3 in politico_stories:
					# gets the titles of each of the news headline
					title_text = h3.get_text(strip=True)
					counter += 1
					# print(title_text)
					# title_pic = h3.find('scr')
					# img_src = img['img']

					# gets the link for each of the headline
					link = h3.find('a')
					# checks for the hyperlink and then prints it
					if link and link.get('href'):
						href = link['href']
						print(f"Title: {title_text}")
						print(f"Link: {href}")
						# print(f"Picture Link: {img_src}")
						print('---')
						print(f"The Number of articles from Politico: {counter}")
				# for each story in stories
				# print(stories)
				
			# except 
			except: 
				pass



# Testing 
for website in websites:
	result = extract_content(website)
	print(result)
