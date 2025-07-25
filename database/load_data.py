import pandas as pd #is panda a valid module?
import pymysql
#import sanitize_electric as electric
#import sanitize_gas as gas
#Import date and timedelta class
# from datetime module
from datetime import date
from datetime import timedelta



#get yesterdays date and make it a string
#ask farid about is the file name date of collection or date of upload
def get_filename():
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
    return filename

def push_to_sql(df, database_name):
    # Database connection parameters
    db_config = {
        'user': 'u209446640_SSUTeam',          # Replace with your database username
        'password': 'SsuIot!432',                 # Replace with your database password
        'host': '193.203.166.234',              # Use the correct database host
        'database': 'u209446640_SSUEnergy',     # Replace with your actual database name
        'port': 3306,                           # Specify the port (default is 3306)
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

    # Step 3: Insert data into the database in batches
    insert_query = f"""
    INSERT INTO {database_name} (time_stamp, location, energy_usage, electric_or_gas)
    VALUES (%s, %s, %s, %s)
    """

    #degree report is different
    degree_insert = f"""
    INSERT INTO {database_name} (time_stamp, heating_usage, cooling_usage)
    VALUES (%s, %s, %s)
    """

    # Prepare to batch insert
    batch_data = []

    for index, row in df.iterrows():
        batch_data.append((row['time_stamp'], row['location'], row['energy_usage'], row['electric_or_gas']))
        
        # When batch size is reached, execute the insert
        try:
            cursor.executemany(insert_query, batch_data)
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
