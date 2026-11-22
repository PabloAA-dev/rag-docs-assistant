import streamlit as st
from ask import ask

st.title("Ask the Deep Learning Book")
st.write("Ask a question about Dive into Deep Learning. Answers cite PDF pages.")

question = st.text_input("Your question")

if question:
    with st.spinner("Searching the book..."):
        answer = ask(question)
    st.write(answer)