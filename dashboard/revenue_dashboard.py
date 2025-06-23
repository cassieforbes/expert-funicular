import pandas as pd
import streamlit as st
import sqlite3
from pathlib import Path
from datetime import datetime

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "revenue.csv"
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "revenue.db"

def load_data_from_csv(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load daily revenue records from a CSV file."""
    return pd.read_csv(path, parse_dates=["Date"])

def load_data_from_db(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Load daily revenue records from a SQLite database."""
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT Date, Revenue, RoomsSold, RoomsAvailable FROM revenue", conn,
                         parse_dates=["Date"])
    finally:
        conn.close()
    return df

st.set_page_config(page_title="Hotel Revenue Dashboard", layout="wide")

# Automatically refresh every minute to pick up new data
st.experimental_autorefresh(interval=60_000, key="auto_refresh")

# Choose data source
source = st.sidebar.selectbox("Data Source", ["CSV", "Database"])
if source == "CSV":
    df = load_data_from_csv()
else:
    try:
        df = load_data_from_db()
    except Exception as e:
        st.error(str(e))
        st.stop()

df = df.sort_values("Date")

total_revenue = df["Revenue"].sum()
adr = (df["Revenue"].sum() / df["RoomsSold"].sum()) if df["RoomsSold"].sum() else 0
occupancy = (df["RoomsSold"].sum() / df["RoomsAvailable"].sum()) * 100 if df["RoomsAvailable"].sum() else 0

st.title("Hotel Revenue Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Average Daily Rate", f"${adr:,.2f}")
col3.metric("Occupancy", f"{occupancy:.1f}%")

st.subheader("Daily Revenue")
st.line_chart(df.set_index("Date")["Revenue"])

st.subheader("Rooms Sold vs Available")
st.area_chart(df.set_index("Date")[["RoomsSold", "RoomsAvailable"]])
