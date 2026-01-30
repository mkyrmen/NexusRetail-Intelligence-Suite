import pandas as pd
import sqlite3

def process_sales():
    df = pd.read_csv("Z:/Project/Sales_Analytics/raw_data/raw_sales.csv")
    
    # 1. Feature Engineering: Create a 'Profit Margin' column
    df['Profit_Margin'] = (df['Profit'] / df['Sales']).round(4)
    
    # 2. Date Dimension: Extract Year and Month for Time-Series analysis
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Year'] = df['Order_Date'].dt.year
    df['Month'] = df['Order_Date'].dt.month
    
    # 3. Load to SQL Database for BI Connection
    conn = sqlite3.connect("Z:/Project/Sales_Analytics/sales_warehouse.db")
    df.to_sql('fct_sales', conn, if_exists='replace', index=False)
    conn.close()
    
    print("🚀 Data cleaned and loaded to SQL Warehouse.")

if __name__ == "__main__":
    process_sales()