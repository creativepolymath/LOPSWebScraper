import streamlit as st
from langchain_community.llms import Ollama
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define a template for the parsing instructions
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Numerical Data Priority:** Dates, numbers, and quantitative information are important."
    "6. **Table Design:** If the information is tabular, format it as a table with appropriate headers."
)

# Initialize the Ollama language model with a specific version
#model = Ollama(model="llama3.2")
model = OllamaLLM(model="llama3.2")

def parse_with_ollama(dom_content, parse_description):
    """
    Parse the given DOM content using the Ollama language model based on the provided description.

    Args:
        dom_content (list): A list of strings, each representing a chunk of the DOM content.
        parse_description (str): A description of what information to extract from the DOM content.

    Returns:
        str: The parsed results as a single string.
    """
    
    # Create a prompt chain using the template
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    parsed_results = []
    
    # Display a spinner while parsing the content
    with st.spinner("Parsing the content..."):
        # Iterate over each chunk of DOM content
        for i, chunk in enumerate(dom_content, start=1):
            # Invoke the model with the current chunk and description
            response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
            
            # Log the progress of parsing
            print(f"Parsed batch {i} of {len(dom_content)}")
            
            # Append the response to the results
            parsed_results.append(response)
        
    # Join all parsed results into a single string
    return "\n".join(parsed_results)
