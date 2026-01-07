import streamlit as st
import shutil
from pathlib import Path

def create_year_archive():
    if Path("LedgerApp").exists():
        shutil.make_archive("LedgerApp_Full", 'zip', "LedgerApp")
        return Path("LedgerApp_Full.zip")
    return None
