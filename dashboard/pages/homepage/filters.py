# dashboard/pages/homepage/filters.py

from dash import html, dcc
from data.constants import (location_options, default_locations,
                                    unit_options, default_units,
                                    timestamp_options, default_min_timestamp, default_max_timestamp)

# filters section
filters = html.Div([
    html.H2("Filters", style={'textAlign': 'center'}),


    html.Div([
        html.Div([
            html.Label(
                "Location",
                style={'fontWeight': 'bold', 'fontSize': '18px'}
            ),
            dcc.Checklist(
                id='location-filter',
                options=location_options,
                value=default_locations,
                labelStyle={'display': 'block', 'textAlign': 'left'}
            )
        ], style={'marginBottom': '40px', 'width': '85%', 'textAlign': 'left'}),

        html.Div([
            html.Label(
                "Unit",
                style={'fontWeight': 'bold', 'fontSize': '18px'}
            ),
            dcc.Checklist(
                id='unit-filter',
                options=unit_options,
                value=default_units,
                labelStyle={'display': 'block', 'textAlign': 'left'}
            )
        ], style={'marginBottom': '40px', 'width': '85%', 'textAlign': 'left'}),

        html.Div([
            html.Label(
                "Timeframe",
                style={'fontWeight': 'bold',
                       'fontSize': '18px',
                       'marginBottom': '5px'}
            ),
            dcc.DatePickerRange(
                id='timestamp-filter',
                # FIX: Assign the date objects directly, without the list lookup.
                start_date=default_min_timestamp,
                end_date=default_max_timestamp,
                min_date_allowed=default_min_timestamp,
                max_date_allowed=default_max_timestamp,
                style={
                'fontSize': '9px',
                'width': '110%'
                }
            )
        ], style={'width': '85%', 'textAlign': 'left'})
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'width': '100%',
    })
],
style={
    'fontFamily': '"Manrope", "Inter", "Segoe UI", sans-serif',
    'fontSize': '16px'
})