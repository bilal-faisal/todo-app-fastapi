import requests
import streamlit as st

st.set_page_config(
    page_title="My Todos",
    page_icon="📝",
)

st.markdown("## My Todos")

# Check if user is logged in
if 'user_id' not in st.session_state:
    st.write("Please add yourself as a user to see your Todos.")
    st.stop()

user_id: str = str(st.session_state.user_id)

req = requests.get("http://localhost:8000/todos", headers={"user-id":user_id})
res = req.json()

if res["status"] == "success":
    todos: list[dict] = res["todos"]
    st.dataframe(todos)