from dash import html, dcc

from data.constants import (building_timestamp_data)

def filters_layout(building_name, frequency="daily"):

    display_name = building_name.replace("_", " ")
    building_key = display_name  

    slider_data = building_timestamp_data[building_key][frequency]

    # frequency dropdown component
    frequency_dropdown = dcc.Dropdown(
        id='time-frequency-dropdown',
        options=[
            {'label': 'Daily', 'value': 'daily'},
            {'label': 'Monthly', 'value': 'monthly'},
            {'label': 'Yearly', 'value': 'yearly'}
        ],
        value=frequency,
        clearable=False,
        style={'width': '50%'}
    )

    # range slider component
    range_slider = dcc.RangeSlider(
        id='time-range-slider',
        min=slider_data['min_index'],
        max=slider_data['max_index'],
        value=[slider_data['min_index'], slider_data['max_index']],
        marks=slider_data['marks'],
        tooltip={"placement": "bottom", "always_visible": False},
        allowCross=False
    )

    # filters section
    filters = html.Div([
        html.H2("Filters", style={'textAlign' : 'center'}),

        html.Div([
            html.Div([
                html.Label("Time Frequency", style={'fontWeight': 'bold'}),
                frequency_dropdown,

                html.Label(
                    "Timeframe", 
                    style={'fontWeight': 'bold', 
                        'fontSize': '18px', 
                        'marginBottom': '5px'}
                ),
                range_slider
                
            ], style={'width': '85%', 'textAlign': 'center'})
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'center',
            'width': '100%',
        })
    ],
    style={
        'fontFamily': '"Manrope", "Inter", "Segoe UI", sans-serif',
        'fontSize': '16px'
    })

    return filters
