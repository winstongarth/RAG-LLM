from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings


def get_embeddings_function():
    embeddings = OpenAIEmbeddings()
    #embeddings = BedrockEmbeddings(credentials_profile_name="default", region_name="us-east-1")
    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings