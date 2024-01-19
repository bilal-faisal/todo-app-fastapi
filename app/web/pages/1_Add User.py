import requests
import streamlit as st
import re

# function to validate email
def validate_email(email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(pattern, email):
        return True
    else:
        return False


st.set_page_config(
    page_title="Create User",
    page_icon="👨‍💼",
)

st.markdown("### Identify yourself as a User")

name:str = st.text_input(label="Name", placeholder="Enter your name")
email:str = st.text_input(label="Email", placeholder="Enter your email")

button = st.button("Submit")
error: bool = False

if button:
    if not name:
        st.error("Error: Name is required")
        error = True
    if not email:
        st.error("Error: Email is required")
        error = True
    elif not validate_email(email):
        st.error("Error: Invalid email")
        error = True
    
    if not error:
        req = requests.post("http://localhost:8000/user", json={"name": name, "email": email})
        res = req.json()

        if res["status"] == "success" or "existing_user":
            user_name:str = name
            user_id:int = int(res["user_id"])
            
            # if user already exists, set user_name to existing name
            if res["status"] == "existing_user":
                st.success(f"User already exists!")            
                user_name = res["name"]
            else:
                st.success(f"User created successfully!")

            st.session_state.user_id = int(res['user_id'])
            st.session_state.user_name = user_name
        
        else:
            st.error(f"Error: {res['message']}")