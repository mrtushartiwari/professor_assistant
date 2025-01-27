# from langchain.tools import Tool

import requests
from dotenv import load_dotenv
import os

load_dotenv()

def create_new_students_record(student_name: str, student_id: int) -> str:
    url = "http://localhost:8000/students"
    payload = {"name": student_name, "student_id": student_id}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def get_students_record(student_id: int) -> str:
    url = f"http://localhost:8000/students/{student_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"
    
# get student by name
def get_student_by_name(student_name: str) -> str:
    url = f"http://localhost:8000/students/name/{student_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# delete student by name
def delete_student_by_name(student_name: str) -> str:
    url = f"http://localhost:8000/students/name/{student_name}"
    response = requests.delete(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"
    
# Add scores
def add_score(student_id: int, subject: str, score: int) -> str:
    url = f"http://localhost:8000/scores/{student_id}/{subject}"
    payload = {"subject": subject, "score": score}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"
# Add socre  by name
def add_score_by_name(name: str, subject: str, score: int) -> str:
    url = f"http://localhost:8000/scores/name/{name}"
    payload = {"subject": subject, "score": score}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"
# Read Scores
def read_score(student_id: int, subject: str) -> str:
    url = f"http://localhost:8000/scores/{student_id}/{subject}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Summarize by student name
def summarize_marks_by_name(student_name: str) -> str:
    url = f"http://localhost:8000/summarize_by_student_name/{student_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Summarize by student id 
def summarize_marks_by_id(student_id: int) -> str:
    url = f"http://localhost:8000/summarize_by_student_id/{student_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

#  Summarize by subject
def summarize_marks_by_subject(subject: str) -> str:
    url = f"http://localhost:8000/summarize_by_subject/{subject}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"




# Define a mapping of intents to tools
INTENT_MAPPING = {
    "create_new_students_record": {
        "function": create_new_students_record,
        # "description": "Create a new record student record with a student name and student id",
        # "parameters": ["name", "student_id"]
    },

    "get_students_record": {
        "function": get_students_record,
        # "description": "Create a new record student record with a student name and student id",
        # "parameters": ["name", "student_id"]
    },

    "get_student_by_name": {
        "function": get_student_by_name,
    },

    "delete_student_by_name": {
        "function": delete_student_by_name,
    },


    "add_score": {
        "function": add_score,
    },
    "read_score": {
        "function": read_score,
    },

    "add_score_by_name": {
        "function": add_score_by_name,
    },

    

    "summarize_marks_by_id": {
        "function": summarize_marks_by_id,
    },

    "summarize_marks_by_name": {
        "function": summarize_marks_by_name,
    },

    "summarize_marks_by_subject": {
        "function": summarize_marks_by_subject,
    }
}


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",api_key=os.environ["GEMINI_API_KEY"])

from langchain.prompts import PromptTemplate

# Define a prompt template to extract intent and parameters
intent_extraction_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
    Analyze the following user query and extract the intent and parameters.

    User Query: {query}
    
    Intent (choose from: 'create_new_students_record','get_students_record','get_student_by_name','delete_student_by_name',
 'add_score','read_score','summarize_marks_by_id','summarize_marks_by_name','summarize_marks_by_subject'):
    Parameters (in JSON format):
    """
)

# Example usage
# query = "Eve's marks performance info"
# query = "Eve marks in Maths"
# query = "what is the average marks in Maths."
# prompt = intent_extraction_prompt.format(query=query)

# # Use Gemini to generate the response
# response = llm.invoke(prompt)
# print(response)



import json
import re
from typing import List

from langchain_core.messages import AIMessage
# Custom parser
def extract_json(message: AIMessage) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between \`\`\`json and \`\`\` tags.

    Parameters:
        text (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON strings.
    """
    text = message.content
    # Define the regular expression pattern to match JSON blocks
    pattern = r"\`\`\`json(.*?)\`\`\`"

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")
    
# Write a parser to get the fuction name as well
def extract_function_name(message: AIMessage) -> str:
    """Extracts the function name from a string.

    Parameters:
        text (str): The text containing the function name.

    Returns:
        str: The extracted function name.
    """
    text= message.content

    t1, t2 = text.split("Parameters")
    t1 = t1.strip()
    _,t1 = t1.split(':')
    t1 = t1.strip()
    if '`' in t1:
        string_without_backticks = t1.replace('`', '')
    else:
        string_without_backticks = t1
    

    try:
        return string_without_backticks
    except Exception:
        raise ValueError(f"Failed to parse: {message}")


# Write a function to input a query and return response after finding out the intent and parameters
def run_query(query: str) -> str:
    # Use Gemini to generate the response
    prompt = intent_extraction_prompt.format(query=query)
    response = llm.invoke(prompt)
    # print(response)
    parameters =extract_json(response)[0]
    function_name = extract_function_name(response)

    if function_name in INTENT_MAPPING:
    # Get the function
        func = INTENT_MAPPING[function_name]["function"]
        # print(func, parameters)
        print(func(**parameters))
    else:
        print(f"Function '{function_name}' not found in the mapping.")


run_query(query= "Average marks in Maths")

# TODO Make run_query into gradio app
