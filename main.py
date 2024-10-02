import streamlit as st
from scrape import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from parse import parse_with_ollama

# Set the title of the Streamlit app
st.title("Python AI Web Scraper")

# Input field for the user to enter the website URL
url = st.text_input("Enter Website URL:")

# Check if the "Scrape" button is pressed
if st.button("Scrape"):
    st.write("scraping the site")
    
    # Scrape the website content
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
            st.write("parsing the content")
            
            # Split the DOM content into chunks
            dom_chunks = split_dom_content(st.session_state.dom_content)
            
            # Parse the content using the provided description
            result = parse_with_ollama(dom_chunks, parse_description)
            
            # Display the parsing result
            st.write(result)
            
