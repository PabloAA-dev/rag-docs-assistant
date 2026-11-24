import streamlit as st
from ask import ask

MAX_QUESTIONS = 10

st.title("Ask the Deep Learning Book")
st.write("Ask a question about Dive into Deep Learning. Answers cite PDF pages.")

if "count" not in st.session_state:
    st.session_state.count = 0

question = st.text_input("Your question")

if question:
    if st.session_state.count >= MAX_QUESTIONS:
        st.warning("Demo limit reached. Thanks for trying it!")
    else:
        with st.spinner("Searching the book..."):
            answer = ask(question)
        st.session_state.count += 1
        st.write(answer)