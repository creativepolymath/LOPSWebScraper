import streamlit as st
import pandas as pd
from scrape import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from parse import parse_with_ollama

st.logo("./assets/PolymathTriangle.png", size='large', link=None )

# Set the title of the Streamlit app
st.title("L.O.P.S. - Web Scraper")
'Web scraping with L.angchain, O.llama, P.ython, and S.treamlit'

# Input field for the user to enter the website URL
url = st.text_input("Enter Website URL:")

# Check if the "Scrape" button is pressed
if st.button("Scrape", ):
    #st.write("scraping the site")
    
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
            
            # Parse the content using the provided description
            result = parse_with_ollama(dom_chunks, parse_description)
            
                    # Display the parsing result
            st.write(result)
            
                    # Convert the result to a pandas DataFrame, handling different formats
            if isinstance(result, list):
                if all(isinstance(item, dict) for item in result):
                    df = pd.DataFrame(result)
                else:
                    df = pd.DataFrame(result, columns=['Data'])
            elif isinstance(result, dict):
                    df = pd.DataFrame([result])
            else:
                    df = pd.DataFrame([{'Data': str(result)}])
            
                    # Add a download button for the CSV file
                    csv = df.to_csv(index=False)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name="parsed_data.csv",
                        mime="text/csv",
                    )            
