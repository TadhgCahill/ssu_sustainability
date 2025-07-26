# dashboard/data/constants.py

import pandas as pd
import json
import os
from .csv_source import df

##################################################################################################
#                                      HOMEPAGE CONSTANTS
##################################################################################################

# Truncate location helper
def truncate_name(name):
    if not isinstance(name, str):
        return None
    name_lower = name.lower()
    if "green music center" in name_lower:
        return "Green Music Center"
    elif "ives hall" in name_lower:
        return "Ives Hall"
    elif "nichols hall" in name_lower:
        return "Nichols Hall"
    elif "physical education" in name_lower:
        return "Physical Education"
    elif "rachel carson hall" in name_lower:
        return "Rachel Carson Hall"
    elif "student health center" in name_lower:
        return "Student Health Center"
    elif "student center" in name_lower:
        return "Student Center"
    elif "wine spectator" in name_lower:
        return "Wine Spectator Center"
    elif "campus wide" in name_lower:
        return "Campus Wide"
    else:
        return None

# Wrap all dataframe operations in a check to prevent crashing if db is empty
if not df.empty:
    df['truncated_location'] = df['location'].apply(truncate_name)

    location_grouped = (
        df[df['truncated_location'].notnull()]
        .groupby('truncated_location')['energy_usage']
        .sum()
        .reset_index()
    )

    # FIX: Use cleaner labels for the filter options, without the energy values.
    location_options = [
        {'label': f"{row['truncated_location']}", 'value': row['truncated_location']}
        for _, row in location_grouped.iterrows()
    ]
    default_locations = [opt['value'] for opt in location_options]

    unit_options = []
    if 'unit' in df.columns:
        for unit in sorted(df['unit'].unique()):
            unit_options.append({'label': unit, 'value': unit})

    # FIX: Make the default units dynamic to include all available units on startup.
    default_units = [opt['value'] for opt in unit_options]

    timestamp_options = sorted(df['date_only'].unique())
    default_min_timestamp = timestamp_options[0] if timestamp_options else None
    default_max_timestamp = timestamp_options[-1] if timestamp_options else None
else:
    # Provide empty defaults if df fails to load, so the app can still start
    location_options, default_locations = [], []
    unit_options, default_units = [], []
    timestamp_options, default_min_timestamp, default_max_timestamp = [], None, None

##################################################################################################
# load building GeoJSON file
try:
    current_dir = os.path.dirname(__file__)
    geojson_path = os.path.abspath(os.path.join(current_dir, '..', 'assets', 'geo-json-buildings.json'))
    with open(geojson_path, 'r') as file:
        geo_json_buildings = json.load(file)
except FileNotFoundError:
    print(f"FATAL ERROR: Could not find geo-json-buildings.json at {geojson_path}")
    geo_json_buildings = {}

# get lon and lat of building centers from geojson file
building_centers = {}
if geo_json_buildings:
    for feature in geo_json_buildings.get('features', []):
        properties = feature.get('properties', {})
        building_id = properties.get('id')
        lon = properties.get('center_lon')
        lat = properties.get('center_lat')
        if building_id:
            building_centers[building_id] = (lat, lon)

##################################################################################################
#                                  BUILDINGS PAGE CONSTANTS
##################################################################################################
building_timestamp_data = {}
if not df.empty:
    df_buildings = df.copy()

    # Ensure 'time_stamp' is datetime before proceeding
    df_buildings['time_stamp'] = pd.to_datetime(df_buildings['time_stamp'])
    df_buildings['time_only'] = df_buildings['time_stamp'].dt.time
    df_buildings['month'] = df_buildings['time_stamp'].dt.to_period('M').dt.to_timestamp()
    df_buildings['year'] = df_buildings['time_stamp'].dt.year

    valid_buildings = df_buildings['truncated_location'].dropna().unique()

    for building in valid_buildings:
        filtered = df_buildings[df_buildings['truncated_location'] == building].copy()

        daily_energy = filtered.groupby('date_only')['energy_usage'].sum().reset_index().sort_values('date_only')
        daily_dates = daily_energy['date_only'].tolist()
        daily_marks = {i: date.strftime('%Y-%m-%d') for i, date in enumerate(daily_dates) if i % max(1, len(daily_dates) // 10) == 0}

        monthly_energy = filtered.groupby('month')['energy_usage'].sum().reset_index().sort_values('month')
        monthly_dates = monthly_energy['month'].dt.date.tolist()
        monthly_marks = {i: date.strftime('%Y-%m') for i, date in enumerate(monthly_dates) if i % max(1, len(monthly_dates) // 10) == 0}

        yearly_energy = filtered.groupby('year')['energy_usage'].sum().reset_index().sort_values('year')
        yearly_dates = yearly_energy['year'].astype(str).tolist()
        yearly_marks = {i: date for i, date in enumerate(yearly_dates)}

        building_timestamp_data[building] = {
            'daily': {'data': daily_energy, 'min_index': 0, 'max_index': len(daily_energy) - 1 if not daily_energy.empty else 0, 'marks': daily_marks},
            'monthly': {'data': monthly_energy, 'min_index': 0, 'max_index': len(monthly_energy) - 1 if not monthly_energy.empty else 0, 'marks': monthly_marks},
            'yearly': {'data': yearly_energy, 'min_index': 0, 'max_index': len(yearly_energy) - 1 if not yearly_energy.empty else 0, 'marks': yearly_marks}
        }