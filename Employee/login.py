import streamlit as st
import json
from pathlib import Path

st.title("Employee Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    emp = next((e for e in emp_db if e["username"] == username and e["password"] == password), None)
    if emp:
        if emp["verified"]:
            st.success(f"Welcome {emp['name']}!")
            st.session_state["selected_emp"] = emp["name"]
            st.experimental_rerun()
        else:
            st.warning("Your account is not verified yet.")
    else:
        st.error("Invalid username or password")
