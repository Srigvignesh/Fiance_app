# helper.py
from pathlib import Path
import zipfile
import pandas as pd
from io import BytesIO
import pyperclip
import shutil
from pathlib import Path
import zipfile

# Existing helper functions
def empty_df():
    COLUMNS = ["S.NO", "NAME", "Mobile Number", "AMOUNT"]
    return pd.DataFrame([{c: "" for c in COLUMNS}])

def auto_sno(df):
    df = df.copy()
    df["S.NO"] = range(1, len(df) + 1)
    return df

def copy_df(df):
    pyperclip.copy(df.to_csv(index=False))

def df_to_excel_bytes(df):
    buf = BytesIO()
    auto_sno(df).to_excel(buf, index=False)
    buf.seek(0)
    return buf

def create_data_archive(year, emp_name=None):
    """
    Create a zip archive for the given year.
    If emp_name is provided, archive only that employee's data.
    """
    base_path = Path("data") / str(year)
    if emp_name:
        base_path = base_path / emp_name  # Folder structure: data/<year>/<employee>/
        if not base_path.exists():
            return None

    archive_name = Path(f"{emp_name}_{year}_ledger_data.zip") if emp_name else Path(f"{year}_ledger_data.zip")

    with zipfile.ZipFile(archive_name, "w") as zipf:
        if emp_name:
            for file in base_path.rglob("*.*"):
                zipf.write(file, arcname=file.relative_to(base_path.parent))
        else:
            for file in base_path.rglob("*.*"):
                zipf.write(file, arcname=file.relative_to(base_path.parent))
    return archive_name
# # ---------------- Year archive ----------------
# def create_data_archive(year: int, month: str = None, week: str = None) -> Path:
#     """
#     Create a zip archive of ledger data for:
#     - full year if month is None
#     - specific month if week is None
#     - specific week if week is provided
#     Returns path to ZIP file
#     """
#     base_dir = Path("data") / str(year)
#     if not base_dir.exists():
#         return None
#
#     archive_dir = Path("temp_archive")
#     if archive_dir.exists():
#         shutil.rmtree(archive_dir)
#     archive_dir.mkdir(parents=True)
#
#     # Decide which folders/files to include
#     if month:
#         month_dir = base_dir / month
#         if not month_dir.exists():
#             return None
#         target_dirs = [month_dir]
#     else:
#         # Full year
#         target_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
#
#     # Copy daily, weekly, monthly files
#     for md in target_dirs:
#         month_archive_dir = archive_dir / md.name
#         month_archive_dir.mkdir(parents=True, exist_ok=True)
#
#         # Daily
#         daily_dir = md / "Daily"
#         if daily_dir.exists():
#             shutil.copytree(daily_dir, month_archive_dir / "Daily", dirs_exist_ok=True)
#
#         # Weekly
#         weekly_file = md / "weekly.xlsx"
#         if weekly_file.exists():
#             shutil.copy(weekly_file, month_archive_dir / "weekly.xlsx")
#
#         # Monthly
#         monthly_file = md / "monthly.xlsx"
#         if monthly_file.exists():
#             shutil.copy(monthly_file, month_archive_dir / "monthly.xlsx")
#
#         # If week is specified, only keep that week in Daily
#         if week:
#             daily_week_dir = month_archive_dir / "Daily"
#             if daily_week_dir.exists():
#                 for day_file in daily_week_dir.iterdir():
#                     if week not in day_file.stem:
#                         day_file.unlink()
#
#     # Create ZIP
#     zip_path = Path(f"Ledger_{year}_{month if month else 'full'}_{week if week else 'all'}.zip")
#     shutil.make_archive(zip_path.stem, 'zip', archive_dir)
#
#     # Cleanup temp
#     shutil.rmtree(archive_dir)
#     return zip_path