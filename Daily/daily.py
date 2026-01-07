import streamlit as st
from datetime import date, timedelta
import calendar
import pandas as pd
from helper import helper

empty_df = helper.empty_df
auto_sno = helper.auto_sno
copy_df = helper.copy_df
df_to_excel_bytes = helper.df_to_excel_bytes

CUSTOM_COLUMNS = ["DISTRIBUTION", "VILLAGE"]

# --- Week generator skipping Thu & Fri ---
def get_month_weeks(year:int, month:int):
    """
    Returns a dict: week_no -> {day_name: date}
    Skips Thursday (3) and Friday (4) as holidays
    """
    weeks = {}
    first = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    last = date(year, month, last_day)
    current = first

    while current <= last:
        if current.weekday() not in (3, 4):  # Skip Thu (3) & Fri (4)
            week_no = ((current.day + first.weekday() - 1)//7) + 1
            weeks.setdefault(week_no, {})
            weeks[week_no][current.strftime("%A")] = current
        current += timedelta(days=1)
    return weeks

def daily_tab_ui(year: int, month: int, month_name: str, session_state: dict):
    """Daily tab: week -> day -> districts -> villages"""
    st.markdown("### 📅 Daily (Week-wise, Mon–Fri)")

    # --- User-defined districts ---
    districts_input = st.text_input(f"Enter districts for {month_name} (comma-separated)", key=f"districts_{month_name}")
    districts = [d.strip() for d in districts_input.split(",") if d.strip()]
    if not districts:
        districts = ["Default District"]

    # --- Villages per district ---
    district_villages = {}
    for district in districts:
        village_input = st.text_input(f"Villages for {district} (comma-separated)", key=f"villages_{district}_{month_name}")
        villages = [v.strip() for v in village_input.split(",") if v.strip()]
        district_villages[district] = villages if villages else ["Default Village"]

    # --- Weeks ---
    month_weeks = get_month_weeks(year, month)
    week_tabs = st.tabs([f"Week-{w}" for w in month_weeks])

    for wi, week_no in enumerate(month_weeks):
        with week_tabs[wi]:
            days = month_weeks[week_no]
            day_tabs = st.tabs([f"{d} ({days[d].strftime('%d-%m-%Y')})" for d in days])

            for di, day in enumerate(days):
                with day_tabs[di]:
                    # --- District tabs ---
                    district_tabs = st.tabs(districts)
                    for dt_idx, district in enumerate(districts):
                        with district_tabs[dt_idx]:
                            # --- Village tabs ---
                            villages = district_villages[district]
                            village_tabs = st.tabs(villages)
                            for v_idx, village in enumerate(villages):
                                with village_tabs[v_idx]:
                                    key = f"{year}_{month_name}_W{week_no}_{day}_{district}_{village}"
                                    if key not in session_state:
                                        df = empty_df()
                                        df["DISTRIBUTION"] = district
                                        df["VILLAGE"] = village
                                        session_state[key] = df

                                    df = st.data_editor(session_state[key], num_rows="dynamic", key=f"ed_{key}")
                                    session_state[key] = auto_sno(df)

                                    c1, c2, c3 = st.columns(3)
                                    with c1:
                                        if st.button("💾 Save", key=f"s_{key}"): st.success("Saved")
                                    with c2:
                                        if st.button("📋 Copy", key=f"c_{key}"):
                                            copy_df(df); st.success("Copied")
                                    with c3:
                                        st.download_button(
                                            "⬇ Download",
                                            df_to_excel_bytes(df),
                                            file_name=f"{year}_{month_name}_{day}_{district}_{village}.xlsx",
                                            key=f"d_{key}"
                                        )
