import requests
import streamlit as st

st.set_page_config(
    page_title="Add Todo",
    page_icon="📝",
)

st.markdown("## Add Todo")

# Check if user is logged in
if 'user_id' not in st.session_state:
    st.write("Please add yourself as a user first to add your Todo.")
    st.stop()

user_id: str = str(st.session_state.user_id)

title:str = st.text_input(label="Todo Title", placeholder="Enter title")
description:str = st.text_area(label="Todo Description", placeholder="Enter description")

button = st.button("Add Todo")
error: bool = False

if button:
    if not title:
        st.error("Title is required")
        error = True
    
    if not error:
        req = requests.post("http://localhost:8000/todo", json={"title": title, "description": description or ""}, headers={"user-id":user_id})
        res = req.json()
        print(res)
        if res["status"] == "success":            
            st.success(f"Todo added successfully! Todo id: {res['todo_id']}")

        else:
            st.error(f"Error: {res['message']}")