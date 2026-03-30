import streamlit as st
from prompt_template import combined_chain

st.title("Email Assistant")

email_topic = st.text_input("Email Topic")
recipient = st.text_input("Recipient")
name = st.text_input("Name")

if st.button("Generate Email"):
    email = combined_chain.invoke({
        "email_topic": email_topic,
        "recipient": recipient,
        "name": name,
    })
    st.markdown(email["final_email"])