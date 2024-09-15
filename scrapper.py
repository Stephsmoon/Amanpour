## Python Web Scrapper ##
# scrapes specified news websites

import re
import os
import json
import urllib
import requests
from bs4 import BeautifulSoup

# News Websites
websites = {
	'New York Times':'https://www.nytimes.com', 
	'Fox News':'https://www.foxnews.com',
	'ABC News':'https://abcnews.go.com', 
	'Washington Post':'https://www.washingtonpost.com',
	'CNN':'https://www.cnn.com'}
# Article Object
class Article:
	def __init__(self, headline, content, link):
		self.headline = headline
		self.content = content
		self.link = link

# Json Correction
def fixjson(jsonString):
	stack = []
	fixed_string = ""
	for char in jsonString:
		if char in '{[':
			stack.append(char)
		elif char in '}]':
			if stack:
				if (stack[-1] == '{' and char == '}') or (stack[-1] == '[' and char == ']'):
					stack.pop()
				else:
					continue
			else:
				continue
		fixed_string += char
	while stack:
		last_open = stack.pop()
		if last_open == '{':
			fixed_string += '}'
		elif last_open == '[':
			fixed_string += ']'
	return fixed_string

# Extraction Function
def extractContent():
	# dictionary which stores article objects
	stored_content = {}
	# grabs headlines from each website
	for website, url in websites.items():
		# array which will store Article Objects
		storage = []
		# webscrape from new york times
		if website == 'New York Times':
			try:
				# articles to avoid
				avoid = ["upshot", "/opinion/", "/magazine/", "/movies/", "/fashion/", "/games/", "/arts/"]
				# access website
				soup = BeautifulSoup(urllib.request.urlopen(url),'html.parser')
				# grab all stories
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
						# append object
						storage.append(Article(headline,content,grabUrl))
					except: 
						pass
			except Exception as e: 
				print(e)
				pass
			# add new york times articles
			stored_content[website] = storage
		# webscrape from fox news
		if website == 'Fox News':
			try:
				# articles to avoid
				avoid = ["/radio.", "outkick", "/opinion/", "/magazine/", "/video/", "/food-drink/", "/movies/", "/travel/", "/lifestyle/", "/health/", "/sports/", "/entertainment/", "/tech/", "/games", "/politics-cartoons-slideshow"]
				# access website
				soup = BeautifulSoup(urllib.request.urlopen(url),'html.parser')
				# grab all stories
				stories = soup.find_all('h3')
				# for each story in stories
				for story in stories:
					try: 
						grabUrl = story.find('a')['href']
						if not "https:" in grabUrl:
							grabUrl = "https:" + grabUrl
						# check if article is valid
						if re.search("|".join(avoid), grabUrl):
							continue
						# get headline of each of the article
						headline = story.get_text(strip=True)						
					except:
						pass
					try: 
						soup = BeautifulSoup(urllib.request.urlopen(grabUrl),'html.parser')
						# cleanup content
						content = re.search(r'(?<="articleBody": ")(.*?)(?=CLICK TO GET THE FOX NEWS APP)', soup.find('script', type='application/ld+json').string).group(0).strip()
						content = re.sub(r'\\|&nbsp;', '', content).strip()
					except: 
						# return with empty content
						storage.append(Article(headline,"",grabUrl))
						pass
					storage.append(Article(headline,content,grabUrl))
			except Exception as e: 
				print(e)
				pass
			# add fox news articles
			stored_content[website] = storage
		# web scrap for ABC News
		if website == "ABC News":
			try:
				# articles to avoid
				avoid = ["/games/"]
				# access website
				soup = BeautifulSoup(urllib.request.urlopen(url),'html.parser')
				# grab all scripts
				scripts = soup.find_all('script')
				# extract the content of each script tag
				script_contents = [script.string for script in scripts if script.string]
				script_content = "\n".join(script_contents)
				# grab all stories
				stories = re.findall(r'\{"headline":.*?\}', script_content, re.DOTALL)
				# for each story in stories
				for story in stories:
					# json string
					jsonString = fixjson(story.replace("'", '"'))
 					# try to parse
					try:
						# Parse the JSON-like string
						jsonObj = json.loads(jsonString)
						# Extract URL
						grabUrl = jsonObj.get("link")
						# Check if link has a href
						if "href" in grabUrl:
							grabUrl = grabUrl.get("href")
						# check if article is valid
						if re.search("|".join(avoid), grabUrl):
							continue
						# Extract the headline
						headline = jsonObj.get("headline")
					except json.JSONDecodeError:
						print("Error decoding JSON:", jsonString)
					try: 
						soup = BeautifulSoup(urllib.request.urlopen(grabUrl),'html.parser')
						# cleanup content
						content = re.search(r'"body":"(.*?)(?<!\\)"', soup.find('script', text=re.compile(r'"body":')).string, re.DOTALL).group(1)
						content = re.sub(r'<.*?>', '', content)					
					except:
						# return with empty content
						storage.append(Article(headline,"",grabUrl))
						pass
					storage.append(Article(headline,content,grabUrl))
			except Exception as e: 
				print(e)
				pass
			# add abs news articles
			stored_content[website] = storage
	return stored_content

extractContent()
