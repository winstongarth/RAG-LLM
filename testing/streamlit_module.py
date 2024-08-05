import argparse
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma"

ANSWER_PROMPT_TEMPLATE = ...
SUMMARIZE_PROMPT_TEMPLATE = ...

def process_query(mode, query_text):
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)  # top 3 results
    if len(results) == 0 or results[0][1] < 0.7:
        return "Unable to find matching results.", None

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = None

    if mode == "answer":
        prompt_template = ChatPromptTemplate.from_template(ANSWER_PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
    elif mode == "summarize":
        prompt_template = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    return response_text, sources