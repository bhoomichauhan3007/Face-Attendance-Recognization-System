import csv
from datetime import datetime
import os
import pandas as pd

ATTENDANCE_FILE = "attendance/attendance.csv"

def init_attendance_file():
    """Ensure the attendance CSV exists with proper headers"""
    os.makedirs(os.path.dirname(ATTENDANCE_FILE), exist_ok=True)
    
    needs_header = False
    has_lecture_column = True
    
    if not os.path.isfile(ATTENDANCE_FILE):
        needs_header = True
    else:
        # Check if file is empty or missing headers
        try:
            with open(ATTENDANCE_FILE, "r") as f:
                content = f.read().strip()
                if len(content) == 0:
                    needs_header = True
                else:
                    header = content.split("\n")[0]
                    if "Name" not in header:
                        needs_header = True
                    if "Lecture" not in header:
                        has_lecture_column = False
        except:
            needs_header = True
    
    if needs_header or not has_lecture_column:
        if os.path.isfile(ATTENDANCE_FILE) and not needs_header and not has_lecture_column:
            try:
                df = pd.read_csv(ATTENDANCE_FILE)
                if 'Lecture' not in df.columns:
                    df['Lecture'] = 'Unknown'
                df.to_csv(ATTENDANCE_FILE, index=False)
                return
            except Exception:
                pass
        
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Date", "Time", "Lecture"])

def mark_attendance(name, lecture):
    if name == "Unknown":
        return
        
    init_attendance_file()
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    try:
        df = pd.read_csv(ATTENDANCE_FILE)
        # Check if name is already present today for THIS lecture
        today_records = df[(df['Date'] == current_date) & (df['Lecture'] == lecture)]
        if name in today_records['Name'].values:
            return  # Already marked
    except Exception:
        pass  # If read fails, just append

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, current_date, current_time, lecture])

def get_attendance():
    init_attendance_file()
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
        if df.empty:
            return []
        df = df.sort_values(by=["Date", "Time"], ascending=[False, False])
        if 'Lecture' in df.columns:
            df['Lecture'] = df['Lecture'].fillna('Unknown')
        return df.to_dict('records')
    except Exception:
        return []

def get_today_count(lecture=None):
    init_attendance_file()
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
        if df.empty:
            return 0
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if lecture and 'Lecture' in df.columns:
            today_records = df[(df['Date'] == current_date) & (df['Lecture'] == lecture)]
        elif 'Lecture' not in df.columns and lecture:
            return 0
        else:
            today_records = df[df['Date'] == current_date]
            
        return len(today_records['Name'].unique())
    except Exception:
        return 0
