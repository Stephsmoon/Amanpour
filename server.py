## Python Backend Server ##
# Using either RestAPI or RPC Server
# RPCServer : https://safjan.com/how-to-use-rpc-in-python/#:~:text=To%20use%20RPC%20in%20Python%2C%20you%20need%20to%20create%20a,and%20call%20these%20functions%20remotely.
# RestfulAPI : https://cto.ai/blog/building-a-restful-api-with-python/ 

from wrapper import *
from scrapper import *
from difflib import SequenceMatcher

# Article Object
class SummarizedArticle:
	def __init__(self, headline, summary, images, links):
		self.headline = headline
		self.content = content
		self.images = images
		self.links = links

# Backend Functions
def obtainSummaries():
	content = extractContent()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

obtainSummaries()