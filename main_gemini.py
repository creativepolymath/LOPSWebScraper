import streamlit as st
from scrape import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from langchain_gemini.llms import Gemini
from langchain_core.prompts import ChatPromptTemplate

st.logo("./assets/PolymathTriangle.png", size='large', link=None )

# Set the title of the Streamlit app
st.title("Python AI Web Scraper")

# Input field for the user to enter the website URL
url = st.text_input("Enter Website URL:")

# Check if the "Scrape" button is pressed
if st.button("Scrape", ):
    st.write("scraping the site")
    
    # Display a spinner while scraping the website content
    with st.spinner("Scraping the website..."):
        result = scrape_website(url)
    
    # Extract the body content from the HTML
    body_content = extract_body_content(result)
    
    # Clean the extracted body content
    cleaned_content = clean_body_content(body_content)
    
    # Store the cleaned content in the session state
    st.session_state.dom_content = cleaned_content
    
    # Display the cleaned DOM content in an expandable text area
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

# Check if there is DOM content stored in the session state
if "dom_content" in st.session_state:
    # Input field for the user to describe what they want to parse
    parse_description = st.text_area("Describe what you want to parse")
    
    # Check if the "Parse" button is pressed
    if st.button("Parse"):
        if parse_description:
            #st.write("parsing the content")
            
            # Split the DOM content into chunks
            dom_chunks = split_dom_content(st.session_state.dom_content)
            
            # Initialize the Gemini language model
            model = Gemini(model="gemini-pro")
            
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
            
            # Create a prompt chain using the template
            prompt = ChatPromptTemplate.from_template(template)
            chain = prompt | model
            
            parsed_results = []
            
            # Display a spinner while parsing the content
            with st.spinner("Parsing the content..."):
                # Iterate over each chunk of DOM content
                for i, chunk in enumerate(dom_chunks, start=1):
                    # Invoke the model with the current chunk and description
                    response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
                    
                    # Log the progress of parsing
                    print(f"Parsed batch {i} of {len(dom_chunks)}")
                    
                    # Append the response to the results
                    parsed_results.append(response)
                
            # Join all parsed results into a single string
            result = "\n".join(parsed_results)
            
            # Display the parsing result
            st.write(result)
