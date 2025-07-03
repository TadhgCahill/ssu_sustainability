import pandas as pd
import re  # Import for regex handling

#remove hardcoding in timestamp vs ts
def csv_to_df(filename):
    df = pd.read_csv(filename)

    #correct formatting for datetime (python and sql)
    timestamp_global = df.columns[0]
    df[timestamp_global] = df[timestamp_global].str.replace(r' Los_Angeles', '', regex=True)
    df[timestamp_global] = pd.to_datetime(df[timestamp_global], format='%Y-%m-%dT%H:%M:%S%z')

    #removes the units in energy numbers
    
    mbtu_to_kwh = 0.29307
    btu_to_kwh = 0.000293
    tonref_to_kwh = 3.51685

    #for electric or gas
    is_electric = 0
    is_gas = 1

    # List of possible locations and units
    locations = df.columns[1:]  # Skip the timestamp column
    
    #shortens all the locations to be more readable
    for location in locations: #maybe not the most efficient
        slash = location.index('/') - 1 #one before /
        location = location[:slash]

    units = ['kWh', 'therm', 'BTU', 'tonref', 'MBTU']

    # Step 3: Create an empty list to store normalized rows
    normalized_data = []

    #will be list of any unknown units
    bad_data = []

    for index, row in df.iterrows():
        timestamp = row[timestamp_global]  # Extract the datetime-converted timestamp
    
        for location in locations:
            usage_value = row[location]
            
            # Only process if the usage value is not empty or NaN
            if pd.notna(usage_value):
                # Extract the numeric value and unit using regex
                match = re.match(r'([\d.]+)([a-zA-Z]+)', str(usage_value))
                if match:
                    value = float(match.group(1))
                    unit = match.group(2)
                    
                    if unit in units:
                        if unit == 'kWh':
                            normalized_data.append([timestamp, location, value, is_electric])
                        elif unit == 'btu' or unit == 'BTU':
                            value = value * btu_to_kwh
                            normalized_data.append([timestamp, location, value, is_gas])
                        elif unit == 'm_btu':
                            value = value * mbtu_to_kwh
                            normalized_data.append([timestamp, location, value, is_gas])
                        elif unit == 'tonref':
                            value = value * unit
                            normalized_data.append([timestamp, location, value, is_electric])
                    else:
                        # If the unit is not recognized, set it to 'unknown'
                        print(unit, " unknown :O")
                        bad_data.append([timestamp, location, value, is_electric]) #may nnot be electric
                        exit(1) #ask if we wanna skip instead of crash

    if bad_data:
        for  wrong in bad_data:
            print(*wrong)
    
    return pd.DataFrame(normalized_data, columns=['time_stamp', 'location', 'energy_usage', 'electric_or_gas'])