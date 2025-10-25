# db_connection.py
import pandas as pd
from sqlalchemy import create_engine


host = "localhost"
port = 3306
user = "root"
password = ""
database = "DataScience"

connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

# Try
engine = None
try:
    engine = create_engine(connection_string, pool_recycle=3600)
    with engine.connect() as conn:
        print("✅ Connected to Local MySQL (XAMPP) successfully!")
except Exception as e:
    print(f"Connection to Local MySQL (XAMPP) failed. Check XAMPP services. Error: {e}")

# Load cleaned data
df = None
try:
    csv_path = r"C:\Users\Ashwin\Downloads\SecCheck\data\cleaned_stops.csv"
    df = pd.read_csv(csv_path)
    print("Cleaned data loaded successfully.")
except Exception as e:
    print(f" Error loading cleaned data. Check the file path. Error: {e}")

# Uploading to database
if df is not None and engine is not None:
    try:
        df.to_sql("police_stops", con=engine, if_exists="append", index=False)
        print("Data uploaded successfully to the 'police_stops'!")
    except Exception as e:
        print(f"Error while uploading data to XAMPP MySQL: {e}")
else:
    print("Skipping data upload: Connection or data loading failed.")