import argparse
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from typing import List

from app.get_embbedings import get_embeddings_function

load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if not OPENAI_API_KEY:
    raise ValueError("The OpenAI API key is not set. Check your .env file and environment configuration.")

@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]

CHROMA_PATH = "chroma"

ANSWER_PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

SUMMARIZE_PROMPT_TEMPLATE = """
Summarize the main points from the following context:

{context}
"""

def main(query_text: str, mode: str) -> QueryResponse:
    #DB
    embedding_function = get_embeddings_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    #Retrieval
    results = db.similarity_search_with_relevance_scores(query_text, k=3) # top 3 results
    if len(results) == 0 or results[0][1] < 0.7:
        print("Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    if mode == "answer":
        prompt_template = ChatPromptTemplate.from_template(ANSWER_PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
    elif mode == "summarize":
        prompt_template = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text)

    print(prompt)

    #LLM
    model = ChatOpenAI()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    
    return QueryResponse(
        query_text=query_text, response_text=response_text, sources=sources
    )

if __name__ == "__main__":
    #CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, choices=['answer', 'summarize'], help="Mode of operation: 'answer' or 'summarize'.")
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    mode = args.mode
    query_text = args.query_text
    main(query_text=query_text, mode=mode)
    


   