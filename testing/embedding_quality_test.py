from langchain_openai import OpenAIEmbeddings
from langchain.evaluation import load_evaluator
from dotenv import load_dotenv
import openai
import os

"""

EMBEDDING QUALITY TEST

"""


load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if not OPENAI_API_KEY:
    raise ValueError("The OpenAI API key is not set. Check your .env file and environment configuration.")

def main():
    # Get embedding for a word.
    embedding_function = OpenAIEmbeddings() # or BedrockEmbeddings()
    vector = embedding_function.embed_query("apple")
    print(f"Vector for 'apple': {vector}")
    print(f"Vector length: {len(vector)}")

    # Compare vector of two words
    evaluator = load_evaluator("pairwise_embedding_distance")
    words = ("apple", "iphone")
    x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1])
    print(f"Comparing ({words[0]}, {words[1]}): {x}")


if __name__ == "__main__":
    main()