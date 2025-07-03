import pandas as pd
import re  # Import for regex handling

#remove hardcoding in timestamp vs ts
def csv_to_df(filename):
    df = pd.read_csv(filename)

    #correct formatting for datetime (python and sql)
    timestamp_global = df.columns[0]
    df[timestamp_global] = df[timestamp_global].str.replace(r' Los_Angeles', '', regex=True)
    df[timestamp_global] = pd.to_datetime(df[timestamp_global], format='%Y-%m-%dT%H:%M:%S%z')

    heating = df.columns[1] #works
    cooling = df.columns[2]

    # Step 3: Create an empty list to store normalized rows
    normalized_data = []
    for index, row in df.iterrows():
        timestamp = row[timestamp_global]  # Extract the datetime-converted timestamp
        heating_value = row[heating]
        cooling_value = row[cooling]

        if pd.notna(heating_value):
                # Extract the numeric value and unit using regex
                heat_just_num = re.findall(r'\d+', heating_value)

        if pd.notna(cooling_value):
                # Extract the numeric value and unit using regex
                cool_just_num = re.findall(r'\d+', cooling_value)
        
        normalized_data.append([timestamp, heat_just_num[0], cool_just_num[0]])

    return pd.DataFrame(normalized_data, columns=['time_stamp', 'heating_usage', 'cooling_usage'])