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
messages = [ {"role":"system","content":"Please summarize all given headline and articles into one headline and a three sentence summary. Avoid all political biases and do not hallucinate topics."} ]

# Summarize Function 
def aiSummarize(headlines, articles):
	# unpack content
	message = "provided headlines: " + headlines + " provided articles: " + articles
	# update message
	messages.append({"role":"user","content":message})
	# create response
	chat = client.chat.completions.create(model="gpt-3.5-turbo",messages=messages)
	reply = chat.choices[0].message.content
	return reply
