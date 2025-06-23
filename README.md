# expert-funicular

This repository contains a simple Streamlit dashboard for viewing hotel revenue metrics.

## Running the Dashboard

1. Install dependencies:
   ```bash
   pip install streamlit pandas
   ```
2. Launch the app from the repository root:
   ```bash
   streamlit run dashboard/revenue_dashboard.py
   ```

The dashboard reads daily revenue records from `data/revenue.csv` by default. You can switch to a SQLite database using the sidebar selector. The charts refresh automatically every minute so new data is reflected without restarting the app.
