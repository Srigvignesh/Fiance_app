import streamlit as st
from Daily import daily
from Weekly import weekly
from Monthly import monthly
from helper import helper  # Your helper functions: empty_df, df_to_excel_bytes, etc.

# -------------------------
# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="LedgerApp",
    layout="wide"
)

# -------------------------
# Constants
TAMIL_MONTHS = [
    "ஜனவரி", "பிப்ரவரி", "மார்ச்", "ஏப்ரல்",
    "மே", "ஜூன்", "ஜூலை", "ஆகஸ்ட்",
    "செப்டம்பர்", "அக்டோபர்", "நவம்பர்", "டிசம்பர்"
]

# -------------------------
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

# -------------------------
st.title("OWNER :: PALANI")

# -------------------------
if selected_emp is None:
    st.markdown("### 👥 Employee List")

    # Add new employee
    new_emp = st.text_input("Add New Employee", "")
    if st.button("➕ Add Employee"):
        if new_emp.strip():
            if new_emp.strip() not in all_employees:
                all_employees.append(new_emp.strip())
                st.session_state["all_employees"] = all_employees
                st.success(f"Employee '{new_emp}' added!")
                st.experimental_rerun()
            else:
                st.warning(f"Employee '{new_emp}' already exists!")

    # Select employee from dropdown
    emp = st.selectbox("Select Employee", all_employees)
    if st.button("Open Ledger"):
        st.session_state["selected_emp"] = emp
        st.experimental_rerun()

# -------------------------
else:
    emp = selected_emp
    st.markdown(f"## Ledger for {emp}")

    # Back button
    if st.button("⬅ Back to Employee List"):
        st.session_state["selected_emp"] = None
        st.experimental_rerun()

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

    # Optional: Download full year data
    st.markdown("---")
    st.markdown(f"### 📦 Download Ledger Data for {emp}")

    from helper.helper import create_data_archive  # Make sure helper has this
    archive_path = create_data_archive(YEAR, emp_name=emp)  # Pass employee name

    if archive_path and archive_path.exists():
        with open(archive_path, "rb") as f:
            st.download_button(
                f"⬇ Download {YEAR} Ledger Data for {emp}",
                f,
                file_name=f"{emp}_{YEAR}_ledger_data.zip"
            )
