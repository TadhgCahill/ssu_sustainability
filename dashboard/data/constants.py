from data.csv_source import df
import pandas as pd
import json

##################################################################################################

#                                      HOMEPAGE CONSTANTS

##################################################################################################

# Truncate location helper
def truncate_name(name):
    if "Green Music Center".lower() in name.lower():
        return "Green Music Center"
    elif "Ives Hall".lower() in name.lower():
        return "Ives Hall"
    elif "Nichols Hall".lower() in name.lower():
        return "Nichols Hall"
    elif "Physical Education".lower() in name.lower():
        return "Physical Education"
    elif "Rachel Carson Hall".lower() in name.lower():
        return "Rachel Carson Hall"
    elif "Student Health Center".lower() in name.lower():
        return "Student Health Center"
    elif "Student Center".lower() in name.lower():
        return "Student Center"
    elif "Wine Spectator Learning".lower() in name.lower():
        return "Wine Spectator Center"
    else:
        return None

##################################################################################################
# location options and defaults for homepage filters section
# #location_options = []

# for location in sorted(df['location'].unique()):
#     location_options.append({'label': location, 'value': location})

# default_locations = df['location'].unique().tolist()

df['truncated_location'] = df['location'].apply(truncate_name)

location_grouped = (
    df[df['truncated_location'].notnull()]
    .groupby('truncated_location')['energy_usage']
    .sum()
    .reset_index()
)

location_options = [
    {'label': f"{row['truncated_location']} — {row['energy_usage']:.0f} kWh", 'value': row['truncated_location']}
    for _, row in location_grouped.iterrows()
]
default_locations = [opt['value'] for opt in location_options]

##################################################################################################
# unit options and defaults for homepage filters section
unit_options = []

for unit in sorted(df['unit'].unique()):
    unit_options.append({'label': unit, 'value': unit})

default_units = ['Electric (kWh)', 'Gas (kWh)']

##################################################################################################
# timestamp options, marks (ticks), and options for homepage filters section
timestamp_options = []

# convert to datetime
df['time_stamp'] = pd.to_datetime(df['time_stamp'])

# take out only date
df['date_only'] = df['time_stamp'].dt.date

# get unique dates
timestamp_options = sorted(df['date_only'].unique())

timestamp_marks = {}
for index, timestamp in enumerate(timestamp_options):
    timestamp_marks[index] = timestamp.strftime('%Y-%m-%d')

default_min_timestamp = 0
default_max_timestamp = len(timestamp_options) - 1

##################################################################################################
# load building GeoJSON file
with open('dashboard/assets/geo-json-buildings.json', 'r') as file:
    geo_json_buildings = json.load(file)

# get lon and lat of building centers from geojson file
building_centers = {}
for feature in geo_json_buildings['features']:
    properties = feature['properties']
    building_id = properties['id']
    lon = properties.get('center_lon')
    lat = properties.get('center_lat')
    building_centers[building_id] = (lat, lon)

##################################################################################################

#                                  BUILDINGS PAGE CONSTANTS

##################################################################################################

# copy df to avoid overlapping homepage
df_buildings = df.copy()

# filling df_buildings columns
df_buildings['truncated_location'] = df_buildings['location'].apply(truncate_name)
df_buildings['time_stamp'] = pd.to_datetime(df_buildings['time_stamp'])
df_buildings['date_only'] = df_buildings['time_stamp'].dt.date
df_buildings['time_only'] = df_buildings['time_stamp'].dt.time
df_buildings['month'] = df_buildings['time_stamp'].dt.to_period('M').dt.to_timestamp()
df_buildings['year'] = df_buildings['time_stamp'].dt.year

# dict of filtered dfs by building
building_dataframes = {}

# timestamp data for sliders (daily, monthly, yearly)
building_timestamp_data = {}

valid_buildings = df_buildings['truncated_location'].dropna().unique()

for building in valid_buildings:

    # filter df for a building
    filtered = df_buildings[df_buildings['truncated_location'] == building].copy()
    building_dataframes[building] = filtered

    # energy by DAY
    daily_energy = (
        filtered.groupby('date_only')['energy_usage']
        .sum()
        .reset_index()
        .sort_values('date_only')
    )
    daily_dates = daily_energy['date_only'].tolist()
    daily_marks = {
        i: daily_dates[i].strftime('%Y-%m-%d')
        for i in range(0, len(daily_dates), max(1, len(daily_dates) // 10))
    }

    # energy by MONTH
    monthly_energy = (
        filtered.groupby('month')['energy_usage']
        .sum()
        .reset_index()
        .sort_values('month')
    )
    monthly_dates = monthly_energy['month'].dt.date.tolist()
    monthly_marks = {
        i: monthly_dates[i].strftime('%Y-%m')
        for i in range(0, len(monthly_dates), max(1, len(monthly_dates) // 10))
    }

    # energy by YEAR
    yearly_energy = (
        filtered.groupby('year')['energy_usage']
        .sum()
        .reset_index()
        .sort_values('year')
    )
    yearly_dates = yearly_energy['year'].astype(str).tolist()
    yearly_marks = {
        i: yearly_dates[i]
        for i in range(0, len(yearly_dates), max(1, len(yearly_dates) // 10))
    }

    building_timestamp_data[building] = {
        'daily': {
            'data': daily_energy,
            'min_index': 0,
            'max_index': len(daily_energy) - 1,
            'marks': daily_marks,
        },
        'monthly': {
            'data': monthly_energy,
            'min_index': 0,
            'max_index': len(monthly_energy) - 1,
            'marks': monthly_marks,
        },
        'yearly': {
            'data': yearly_energy,
            'min_index': 0,
            'max_index': len(yearly_energy) - 1,
            'marks': yearly_marks,
        }
    }