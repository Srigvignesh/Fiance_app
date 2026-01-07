import streamlit as st
from Daily import daily
from Weekly import weekly
from Monthly import monthly
from helper import helper  # Your helper functions

st.set_page_config(page_title="LedgerApp", layout="wide")

TAMIL_MONTHS = [
    "ஜனவரி", "பிப்ரவரி", "மார்ச்", "ஏப்ரல்",
    "மே", "ஜூன்", "ஜூலை", "ஆகஸ்ட்",
    "செப்டம்பர்", "அக்டோபர்", "நவம்பர்", "டிசம்பர்"
]

# Session state init
if "session_state" not in st.session_state:
    st.session_state["session_state"] = {}

if "all_employees" not in st.session_state:
    st.session_state["all_employees"] = ["Sri", "Ravi", "Anu", "Kumar"]

if "selected_emp" not in st.session_state:
    st.session_state["selected_emp"] = None

session_state = st.session_state["session_state"]
all_employees = st.session_state["all_employees"]
selected_emp = st.session_state["selected_emp"]

st.title("OWNER :: PALANI")

# -------------------------
# Employee Selection
if selected_emp is None:
    st.markdown("### 👥 Employee List")

    # Add new employee
    new_emp = st.text_input("Add New Employee", "")
    add_clicked = st.button("➕ Add Employee")
    if add_clicked and new_emp.strip():
        if new_emp.strip() not in all_employees:
            all_employees.append(new_emp.strip())
            st.session_state["all_employees"] = all_employees
            st.success(f"Employee '{new_emp}' added!")
        else:
            st.warning(f"Employee '{new_emp}' already exists!")

    # Select employee from dropdown
    emp = st.selectbox("Select Employee", all_employees)
    open_clicked = st.button("Open Ledger")
    if open_clicked:
        st.session_state["selected_emp"] = emp
        # No rerun needed, next rerun happens automatically

# -------------------------
# Employee Ledger
else:
    emp = selected_emp
    st.markdown(f"## Ledger for {emp}")

    # Back button
    if st.button("⬅ Back to Employee List"):
        st.session_state["selected_emp"] = None
        # No rerun needed, Streamlit will rerender automatically

    # Year input (no min/max)
    YEAR = st.number_input(
        f"Enter Year for {emp}:",
        value=2026,
        step=1,
        key=f"year_{emp}"
    )

    # Month Tabs
    month_tabs = st.tabs(TAMIL_MONTHS)
    for mi, month_name in enumerate(TAMIL_MONTHS):
        with month_tabs[mi]:
            main_tabs = st.tabs(["Daily", "Weekly", "Monthly"])
            with main_tabs[0]:
                daily.daily_tab_ui(YEAR, mi + 1, month_name, session_state)
            with main_tabs[1]:
                weekly.weekly_tab_ui(YEAR, month_name, session_state)
            with main_tabs[2]:
                monthly.monthly_tab_ui(YEAR, month_name, session_state)
