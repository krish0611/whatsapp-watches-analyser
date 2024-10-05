import streamlit as st
import pandas as pd
import re

def filter_messages(chat_text):
    # Define keywords for filtering messages
    keywords = ["Looking", "Want", "Sold Order", "WTB", "Need", "This message was deleted", "image omitted", "quote", "NTQ"]
    lower_keywords = [keyword.lower() for keyword in keywords]
    
    # Regular expression to identify date and timestamp
    timestamp_pattern = r"\[\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2}(\s?AM|\s?PM)?\]"
    
    lines = chat_text.split("\n")
    filtered_messages = []
    current_message = []
    skip = False
    
    for line in lines:
        lower_line = line.lower()

        # Start a new message when we detect a timestamp
        if re.match(timestamp_pattern, line):
            if current_message:
                full_message = "\n".join(current_message)
                # Add the message if not skipping
                if not skip:
                    filtered_messages.append(full_message)
            current_message = [line]  # Start a new message block
            skip = False  # Reset the skip flag

        # Skip lines if any keyword is present
        elif any(keyword in lower_line for keyword in lower_keywords):
            skip = True

        # If not skipping, append line to the current message
        elif not skip:
            current_message.append(line)
    
    # Add the last message to the filtered messages list
    if current_message and not skip:
        filtered_messages.append("\n".join(current_message))
    
    return filtered_messages

st.title("WhatsApp Chat Filter")

chat_text = st.text_area("Paste your WhatsApp chat here:")
if st.button("Filter Chat"):
    filtered_chat = filter_messages(chat_text)
    
    # Create a DataFrame with the filtered messages
    chat_df = pd.DataFrame(filtered_chat, columns=["Message"])
    
    # Display the DataFrame as a table
    st.dataframe(chat_df)
