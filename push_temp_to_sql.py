import pandas as pd #is panda a valid module?
import pymysql
import sanitize_degree_day as degree
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
    INSERT INTO {database_name} (time_stamp, heating_usage, cooling_usage)
    VALUES (%s, %s, %s)
    """

    # see if offset can be removed
    #change the hard coding

    # Define the batch size

    # Prepare to batch insert
    batch_data = []

    for index, row in df.iterrows():
        batch_data.append((row['time_stamp'], row['heating_usage'], row['cooling_usage']))
        
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

# year1 = '2024'
# year2 = '2025'

# #iterate  11, 12, 1, 2
# #for 12: 31
# for dec in range(4, 31):
#     day = str(dec)
#     if dec< 10:
#         day = '0' + str(dec)
#     filenameTemp = 'degreeDayReports/' + year1 + '12' + day + '.csv'
#     df = degree.csv_to_df(filenameTemp)
#     #push df to sql
#     push_to_sql(df, 'temp_daily')

# #for 1: 31
# for jan in range(1, 31):
#     day = str(jan)
#     if jan< 10:
#         day = '0' + str(jan)
#     filenameTemp = 'degreeDayReports/' + year2 + '01' + day + '.csv'
#     df = degree.csv_to_df(filenameTemp)
#     #push df to sql
#     push_to_sql(df, 'temp_daily')

# #for 2: 11
# for feb in range(1, 11):
#     day = str(feb)
#     if feb< 10:
#         day = '0' + str(feb)
#     filenameTemp = 'degreeDayReports/' + year2 + '02' + day + '.csv'
#     df = degree.csv_to_df(filenameTemp)
#     #push df to sql
#     push_to_sql(df, 'temp_daily')