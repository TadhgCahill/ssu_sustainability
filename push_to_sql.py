import pandas as pd #is panda a valid module?
import pymysql
from sanitize_electric import *
#Import date and timedelta class
# from datetime module
from datetime import date
from datetime import timedelta

#take in parameters insead of hard coding

# Database connection parameters
db_config = {
    'user': 'dummy_user',          # Replace with your database username
    'password': 'dummy_pass',                 # Replace with your database password
    'host': 'dummy_host',              # Use the correct database host
    'database': 'dummy_database',     # Replace with your actual database name
    'port': -1,                           # Specify the port (default is 3306)
    'connect_timeout': 30 
}

# Step 1: Connect to the database
try:
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection successful.")
except pymysql.MySQLError as err:
    print(f"Database connection error: {err}")
    exit(1)

# get Yesterdays date and make it a string
yesterday = date.today() - timedelta(days = 1)
temp_month = str(yesterday.month)
temp_day = str(yesterday.day)
if yesterday.month < 10:
    temp_month = '0' + temp_month
if yesterday.day < 10:
    temp_day = '0' + temp_day
#get pathname and add that
filename = str(yesterday.year) + temp_month + temp_day + '.csv'

df = csv_to_df(filename)

# Step 3: Insert data into the database in batches
insert_query = """
INSERT INTO energy_usage (time_stamp, location, energy_usage, electric_or_gas)
VALUES (%s, %s, %s, %s)
offset 1 row;
"""

#change the hard coding

# Define the batch size
batch_size = 1000  # You can adjust this size based on your needs

# Prepare to batch insert
batch_data = []

for index, row in df.iterrows():
    batch_data.append((row['time_stamp'], row['location'], row['energy_usage'], row['electric_or_gas']))
    
    # When batch size is reached, execute the insert
    if len(batch_data) == batch_size:
        try:
            cursor.executemany(insert_query, batch_data)
            print(f"Inserted batch of {batch_size} rows into the database.")
            batch_data.clear()  # Clear the batch data for the next set
        except pymysql.MySQLError as e:
            print(f"Error inserting batch starting with row {index - len(batch_data) + 1}: {e}")
            continue  # Skip to the next batch on error

# Insert any remaining rows in the last batch
if batch_data:
    try:
        cursor.executemany(insert_query, batch_data)
        print(f"Inserted final batch of {len(batch_data)} rows into the database.")
    except pymysql.MySQLError as e:
        print(f"Error inserting final batch: {e}")

# Commit the transaction
try:
    conn.commit()
    print("Data inserted successfully and committed.")
except pymysql.MySQLError as e:
    print(f"Error committing transaction: {e}")

# Step 4: Clean up
finally:
    if 'cursor' in locals():
        cursor.close()
        print("Cursor closed.")
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")

