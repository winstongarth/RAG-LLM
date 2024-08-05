import os
from dotenv import load_dotenv, dotenv_values 

"""

Test script for Langchain

"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

load_dotenv() 
os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or "sk-proj-CznNInXM9EZxJNbKw5MbT3BlbkFJM30W3gHclO9u1DtCMRKq"


OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if not OPENAI_API_KEY:
    raise ValueError("The OpenAI API key is not set. Check your .env file and environment configuration.")

chat = ChatOpenAI(
    OPENAI_API_KEY=os.environ["OPENAI_API_KEY"],
    model='gpt-3.5-turbo' # 'gpt-4'
)

# Define testing messages
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?"),
    HumanMessage(content="I'd like to understand string theory.")
]

res = chat(messages)
print(res.content)

# add latest AI response to messages
messages.append(res)

# now create a new user prompt
prompt = HumanMessage(
    content="Why do physicists believe it can produce a 'unified theory'?"
)
# add to messages
messages.append(prompt)

# send to chat-gpt
res = chat(messages)

print(res.content)