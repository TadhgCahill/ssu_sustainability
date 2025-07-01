import pandas as pd
import os
from .sql_credentials import SQL_CREDENTIALS
import pymysql
import numpy as np

# path to file's directory
#current_dir = os.path.dirname(__file__)

# building full path to csv
#csv_path = os.path.join(current_dir, 'normalized_data4.csv')

# load csv
#df = pd.read_csv(csv_path)


# connect to the MYSQL database
def connect_to_database():
    try:
        connection = pymysql.connect(
            user=SQL_CREDENTIALS['user'],
            password=SQL_CREDENTIALS['password'],
            host=SQL_CREDENTIALS['host'],
            database=SQL_CREDENTIALS['database'],
            port=SQL_CREDENTIALS['port'],
            connect_timeout=SQL_CREDENTIALS['connect_timeout']
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None
    
# create dataframe from SQL query
connection = connect_to_database()
query = "SELECT * FROM energy_usage"  # Replace with your actual SQL query
if connection:
    # Execute the query and fetch the data into a DataFrame
    df = pd.read_sql(query, connection)
    connection.close()
else:
    print("Failed to connect to the database.")
    df = pd.DataFrame()  # Empty DataFrame in case of connection failure

if 'electric_or_gas' in df.columns:
    df['unit'] = np.where(df['electric_or_gas'].to_numpy() == 0, 'Electric (kWh)', 'Gas (kWh)')
else:
    print("electric_or_gas column not found")
