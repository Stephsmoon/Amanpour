## Python Backend Server ##
# Using either RestAPI or RPC Server
# RPCServer : https://safjan.com/how-to-use-rpc-in-python/#:~:text=To%20use%20RPC%20in%20Python%2C%20you%20need%20to%20create%20a,and%20call%20these%20functions%20remotely.
# RestfulAPI : https://cto.ai/blog/building-a-restful-api-with-python/ 

from wrapper import *
from scrapper import *
from difflib import SequenceMatcher

# Article Object
class SummarizedArticle:
	def __init__(self, headline, summary, links):
		self.headline = headline
		self.summary = summary
		self.links = links

# Aggregate Object
class AggregateArticles:
	def __init__(self, headlines, content, links):
		self.headlines = headlines
		self.contents = content
		self.links = links

# obtain Summary Functions
def obtainSummary():
	summaries = []
	content = extractContent()
	# origins of all articles
	origins = list(content.keys())
	# traverse through each origin
	for origin in origins:
		# get each article from origin
		for article in content[origin]:
			# check similarities score against all other aggregated articles
			aggregate = aggregateArticles(article, origin, content)
			# if aggregate is valid
			if aggregate is None:
				continue
			# summarize aggregate and append to summaries
			summary = createSummary(aggregate)
			summaries.append(summary)

# create Summary Function
def createSummary(aggregate):

	print(aggregate.headlines)


	

	# summarizes with Chatgpt
	summary = aiSummarize(aggregate)
	# check if separator exists
	content = re.split(r'\|', summary)
	# create summarized article
	SummarizedArticle(content[0],content[1],aggregate.links)

def aggregateArticles(article, origin, content): 
	aggregate = AggregateArticles([],[],[])
	# origins of all articles
	curr_origins = list(content.keys())
	# traverse through each origin
	for curr_origin in curr_origins:
		if origin == curr_origin:
			continue
		# get each article from origin
		for curr_article in content[curr_origin]:
			score = simScore(article.headline, curr_article.headline)
			# check if score is high enough to aggregate
			if score >= 50:
				aggregate.headlines.append(curr_article.headline)
				aggregate.contents.append(curr_article.content)
				aggregate.links.append(curr_article.link)
	# check if aggregate has articles
	if not aggregate.headlines:
		return None 
	# include given article
	aggregate.headlines.append(article.headline)
	aggregate.contents.append(article.content)
	aggregate.links.append(article.link)
	return aggregate

# Simiarlity Score Function 
def simScore(headlineA, headlineB):
    score = 100 * SequenceMatcher(None, headlineA, headlineB).ratio()
    return score

obtainSummary()