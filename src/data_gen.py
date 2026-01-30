import pandas as pd
import numpy as np
import os

os.makedirs("Z:/Sales_Analytics/data", exist_ok=True)

# Generate synthetic Enterprise Sales Data
np.random.seed(42)
regions = ['North America', 'EMEA', 'APAC', 'LATAM']
categories = ['Technology', 'Office Supplies', 'Furniture']

data = {
    'Order_ID': [f'CA-2024-{1000+i}' for i in range(500)],
    'Order_Date': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2024-12-31'), 500)),
    'Region': np.random.choice(regions, 500),
    'Category': np.random.choice(categories, 500),
    'Sales': np.random.uniform(100, 5000, 500).round(2),
    'Quantity': np.random.randint(1, 10, 500)
}

df = pd.DataFrame(data)
# Create a profit column with some negative values (for "loss" analysis)
df['Profit'] = (df['Sales'] * np.random.uniform(-0.1, 0.4, 500)).round(2)

df.to_csv("Z:/Project/Sales_Analytics/raw_data/raw_sales.csv", index=False)
print("✅ Enterprise Sales data generated.")