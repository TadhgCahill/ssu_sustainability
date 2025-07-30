from dash import html, dcc
from data.constants import (location_options, default_locations, 
                            unit_options, default_units, 
                            timestamp_options, default_min_timestamp, default_max_timestamp)

# filters section
filters = html.Div([
    html.H2("Filters", style={'textAlign' : 'center'}),


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
                start_date=timestamp_options[default_min_timestamp],
                end_date=timestamp_options[default_max_timestamp],
                min_date_allowed=min(timestamp_options),
                max_date_allowed=max(timestamp_options),
                style={
                'fontSize': '9px',   
                'width': '110%'       
                }
            )
        ], style={'marginBottom' : '50px', 'width': '85%', 'textAlign': 'left'}),

        html.Div([
            html.H2(
                "Mobile App", 
                style={'fontWeight': 'bold', 
                       'marginBottom': '5px'}
            ),
            html.Img(src='assets/qr_code.png', style={'height' : '220px', 'width' : '220px'})
        ], style={
            'marginBottom': '40px', 'width': '85%', 'textAlign': 'center'
        }),
        

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
