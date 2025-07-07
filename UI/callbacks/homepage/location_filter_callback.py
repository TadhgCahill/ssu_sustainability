from data.constants import truncate_name

from dash import Input, Output, callback
from datetime import datetime
from data.csv_source import df

# this callback will change the locations available for a user in the filters section based on the unit and timestamp 
# start and end date selected

@callback(
    Output('location-filter', 'options'),
    Output('location-filter', 'value'),
    Input('unit-filter', 'value'),
    Input('timestamp-filter', 'start_date'),
    Input('timestamp-filter', 'end_date')
)
def update_location_options(selected_units, start_date, end_date):
    if start_date is not None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date is not None:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # filter dataframe by selected units and date 
    filtered = df[
        (df['unit'].isin(selected_units)) & 
        (df['date_only'] >= start_date) & 
        (df['date_only'] <= end_date)
    ].copy()

    # truncated names for grouping
    filtered['truncated_location'] = filtered['location'].apply(truncate_name)

    # remove None locations
    filtered = filtered[filtered['truncated_location'].notnull()]

    # group and sum energy usage
    grouped = filtered.groupby('truncated_location')['energy_usage'].sum().reset_index()

    # options list with labels that include energy usage
    #options = [
    #    {'label': f"{row['truncated_location']} — {row['energy_usage']:.0f} kWh", 'value': row['truncated_location']}
    #    for _, row in grouped.iterrows()
    #]

    options = [
        {'label': f"{row['truncated_location']}", 'value': row['truncated_location']}
        for _, row in grouped.iterrows()
    ]

    # default select all available options
    values = [opt['value'] for opt in options]

    return options, values
