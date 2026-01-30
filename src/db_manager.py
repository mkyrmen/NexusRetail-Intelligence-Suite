import sqlite3
import pandas as pd
import os

def get_dashboard_data():
    # PASTE THE PATH YOU COPIED HERE
    # Ensure you use forward slashes (/) or double backslashes (\\)
    db_path = r'Z:\Project\Sales_Analytics\sales_warehouse.db' # Or whatever you copied

    if not os.path.exists(db_path):
        print(f"❌ STILL NOT FOUND: {db_path}")
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM fct_sales;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['Order_Date'] = pd.to_datetime(df['Order_Date'])
            print(f"✅ Successfully loaded {len(df)} rows.")
        return df
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return pd.DataFrame()