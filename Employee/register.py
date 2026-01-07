import streamlit as st
import json
from pathlib import Path

DB_FILE = Path("Employee/emp_db.json")

# Load DB
if DB_FILE.exists():
    with open(DB_FILE, "r") as f:
        emp_db = json.load(f)
else:
    emp_db = []

st.title("Register New Employee")

name = st.text_input("Full Name")
mobile = st.text_input("Mobile Number")
perm_address = st.text_area("Permanent Address")
tmp_address = st.text_area("Temporary Address")
aadhar = st.text_input("Aadhar Number")
pan = st.text_input("PAN Number")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register Employee"):
    if all([name, mobile, perm_address, tmp_address, aadhar, pan, username, password]):
        # Check username uniqueness
        if any(emp['username'] == username for emp in emp_db):
            st.warning("Username already exists!")
        else:
            emp_db.append({
                "name": name,
                "mobile": mobile,
                "perm_address": perm_address,
                "tmp_address": tmp_address,
                "aadhar": aadhar,
                "pan": pan,
                "verified": False,
                "username": username,
                "password": password
            })
            with open(DB_FILE, "w") as f:
                json.dump(emp_db, f, indent=4)
            st.success(f"Employee {name} added! Pending verification.")
    else:
        st.warning("Please fill all fields")
