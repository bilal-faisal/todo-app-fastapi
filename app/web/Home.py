import streamlit as st

st.set_page_config(
    page_title="Todo App",
    page_icon="📋",
)

st.title("Welcome to Todo App!")

if 'user_name' not in st.session_state:
    st.write("Please add yourself as a user to play along.")
else:
    st.write("Welcome, ", st.session_state.user_name)