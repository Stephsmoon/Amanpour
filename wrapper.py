## Python Chatgpt Wrapper ##
# Wraps Chatgpt to Read Webscrapped New Sources

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()
# open ai key from env
client = OpenAI(api_key=os.getenv('OPENAI_TOKEN'))
# intial message to chatgpt
messages = [ {"role": "system", "content": 
			  "You are a intelligent assistant."} ]

# Validation Error
class validationError(Exception):
	pass

# Summarize Function 
def aiSummarize(article):
	# check whether article is valid 
	if not article:
		raise validationError("bad article")
	# unpack article
	message = article  
	# update message
	messages.append(
		{"role":"user","content":message},
	)
	# create response
	chat = client.chat.completions.create(model="gpt-3.5-turbo",messages=messages)
	reply = chat.choices[0].message.content
	print(f"ChatGPT: {reply}")