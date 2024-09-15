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
messages = [{"role":"system","content":"Please summarize all given headline and articles into one headline and a THREE sentence summary. Avoid all political biases and do not hallucinate topics. The first Sentence will be the Headline."}]

# Summarize Function 
def aiSummarize(articles):
	# unpack headline and update message
	message = "Create Headline with the provided Headlines: " + ';'.join(articles.headlines)
	messages.append({"role":"user","content":message})
	# create response
	chat = client.chat.completions.create(model="gpt-3.5-turbo",messages=messages)
	HeadlineReply = chat.choices[0].message.content
	# add response to reply
	messages.append({"role": "assistant", "content": HeadlineReply})
	# unpack content
	message = "Create Headline with the provided Headlines: " + ';'.join(articles.headlines)
	# unpack Articles and update message
	message = "Create THREE Sentence Summary with the provided articles: " + ';'.join(articles.contents)
	ArticleReply = chat.choices[0].message.content
	# return with separator
	return HeadlineReply + "|" + ArticleReply
