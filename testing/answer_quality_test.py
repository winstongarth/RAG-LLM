from ..src.app.main import main
from langchain_openai import ChatOpenAI

"""
UNIT TESTING

method to try:
-text splitting -> chunk size , optimal num of chunks
-embeddings model
-gpt model
-database format -> convert first to md or use the origainal format
-diffrenciate between notes and exam question for information,
"""

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def test():
    assert query_and_validate(
        question="What is AI?",
        expected_response="AI stands for Artificial Intelligence, which is a technology that enables machines to perform tasks that typically require human intelligence, such as understanding visual signals, recognizing speech, and sensing the physical world through various signals in the Internet of Things (IoT) ecosystem",
    )

def query_and_validate(question: str, expected_response: str):
    response_text = main()
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )


    model = ChatOpenAI()
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
        
        