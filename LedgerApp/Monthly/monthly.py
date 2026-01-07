import streamlit as st
import pandas as pd
from helper import helper

empty_df = helper.empty_df
auto_sno = helper.auto_sno
copy_df = helper.copy_df
df_to_excel_bytes = helper.df_to_excel_bytes

CUSTOM_COLUMNS = ["DISTRIBUTION", "VILLAGE"]

def monthly_tab_ui(year:int, month_name:str, session_state:dict):
    """Monthly summary tab with districts and villages"""
    st.markdown("### 📅 Monthly Summary")

    # --- User-defined districts ---
    districts_input = st.text_input(f"Enter districts for {month_name} (comma-separated)", key=f"monthly_districts_{month_name}")
    districts = [d.strip() for d in districts_input.split(",") if d.strip()]
    if not districts:
        districts = ["Default District"]

    # --- Villages per district ---
    district_villages = {}
    for district in districts:
        village_input = st.text_input(f"Villages for {district} (comma-separated)", key=f"monthly_villages_{district}_{month_name}")
        villages = [v.strip() for v in village_input.split(",") if v.strip()]
        district_villages[district] = villages if villages else ["Default Village"]

    # --- District tabs ---
    district_tabs = st.tabs(districts)
    for dt_idx, district in enumerate(districts):
        with district_tabs[dt_idx]:
            villages = district_villages[district]
            village_tabs = st.tabs(villages)
            for v_idx, village in enumerate(villages):
                with village_tabs[v_idx]:
                    key = f"{year}_{month_name}_monthly_{district}_{village}"
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
                            file_name=f"{year}_{month_name}_monthly_{district}_{village}.xlsx",
                            key=f"d_{key}"
                        )
