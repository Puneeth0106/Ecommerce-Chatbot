import pandas as pd
import sqlite3
from pathlib import Path
import os

# 1. SETUP PATHS CORRECTLY
# Get the directory of the current script (web-scrapping)
current_dir = Path(__file__).resolve().parent
# Go up one level to the project root (Project-ecommerce-tool)
project_root = current_dir.parent

# Define the database directory and path
db_folder = project_root / 'app' / 'resources'
db_path = db_folder / 'ecommerce_data.db'
csv_path = current_dir / 'ecommerce_data_final.csv'

# 2. ENSURE DIRECTORY EXISTS
# This prevents "unable to open database file" error
db_folder.mkdir(parents=True, exist_ok=True)

def insert_data(db_path, csv_path):
    # Check if CSV exists before proceeding
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        return

    # 3. KEEP LOGIC INSIDE THE CONNECTION CONTEXT
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            product_link TEXT,
            title TEXT,
            brand TEXT,
            price INTEGER,
            discount FLOAT,
            avg_rating FLOAT,
            total_ratings INTEGER
        );
        ''')
        # The 'with' context usually handles commits, but explicit commit for DDL is fine
        conn.commit()

        # Read CSV
        print("Reading CSV...")
        df = pd.read_csv(csv_path)
        print(df.head())

        # Insert Data
        print("Inserting data into database...")
        df.to_sql('product', conn, if_exists='append', index=False)
        
        print("Data inserted successfully!")
    # Connection closes automatically here

if __name__ == "__main__":
    insert_data(db_path, csv_path)