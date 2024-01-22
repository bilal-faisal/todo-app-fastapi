import requests
import streamlit as st

st.set_page_config(
    page_title="Edit Todo",
    page_icon="📝",
)

st.markdown("## Edit your Todo")

# Check if user is logged in
if 'user_id' not in st.session_state:
    st.write("Please add yourself as a user first to add your Todo.")
    st.stop()

user_id: str = str(st.session_state.user_id)

todo_id:str = st.text_input(label="Todo ID", placeholder="Enter Todo ID")
title:str = st.text_input(label="Updated Title", placeholder="Updated title")
description:str = st.text_area(label="Updated Description", placeholder="Updated description")

button = st.button("Update Todo")
error: bool = False

if button:
    if not title:
        st.error("Title is required")
        error = True
    
    if not todo_id:
        st.error("Todo id is required")
        error = True

    if not error:
        req = requests.patch("http://localhost:8000/todo", json={"title": title, "description": description or "", "todo_id": todo_id}, headers={"user-id":user_id})
        res = req.json()

        if res["status"] == "error":    
            st.error(f"No todo exists with id: {todo_id}")

        if res["status"] == "success":            
            st.success(f"Todo updated successfully! Todo id: {res['todo_id']}")
