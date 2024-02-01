import requests
import streamlit as st

st.set_page_config(
    page_title="Delete Todo",
    page_icon="📝",
)

st.markdown("## Delete Todo")

# Check if user is logged in
if 'user_id' not in st.session_state:
    st.write("Please add yourself as a user first to add your Todo.")
    st.stop()

user_id: str = str(st.session_state.user_id)

todo_id:str = st.text_input(label="Todo ID", placeholder="Enter Todo ID")

button = st.button("Delete Todo")
error: bool = False

if button:
    if not todo_id:
        st.error("Todo ID is required")
        error = True
    
    if not error:
        req = requests.delete(f"http://localhost:8000/todo/{todo_id}", headers={"user-id":user_id})
        res = req.json()
        
        if res["status"] == "error":            
            st.error(f"No todo exists with id: {todo_id}")

        if res["status"] == "success":            
            st.success(f"Todo deleted successfully!")
