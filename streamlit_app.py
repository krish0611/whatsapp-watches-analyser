import streamlit as st
import pandas as pd

def filter_messages(chat_text):
    keywords = ["Looking", "Want", "Sold Order", "WTB", "Need", "This message was deleted", "image omitted", "quote", "NTQ"]
    lower_keywords = [keyword.lower() for keyword in keywords]
    lines = chat_text.split("\n")
    filtered_lines = []
    skip = False

    for line in lines:
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in lower_keywords):
            skip = True
        elif skip and line.startswith("["):
            skip = False
        if not skip:
            filtered_lines.append(line)

    # Remove empty lines
    filtered_lines = [line for line in filtered_lines if line.strip()]

    return filtered_lines

st.title("WhatsApp Chat Filter")

chat_text = st.text_area("Paste your WhatsApp chat here:")
if st.button("Filter Chat"):
    filtered_chat = filter_messages(chat_text)
    
    # Create a DataFrame with the filtered messages
    chat_df = pd.DataFrame(filtered_chat, columns=["Message"])
    
    # Display the DataFrame as a table
    st.dataframe(chat_df)
