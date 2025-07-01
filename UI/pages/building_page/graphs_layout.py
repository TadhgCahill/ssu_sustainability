from dash import html, dcc
import plotly.express as px
from data.constants import building_timestamp_data

def graphs_layout(building_name, frequency='daily'):
    display_name = building_name.replace("_", " ")
    building_key = display_name

    # aggregated data
    if building_key not in building_timestamp_data:
        return html.Div("no data available.")

    graph_data = building_timestamp_data[building_key][frequency]['data']

    # rename columns for plots
    graph_data = graph_data.rename(columns={
        graph_data.columns[0]: 'Date',
        graph_data.columns[1]: 'Energy'
    })

    # line graph
    line_fig = px.line(graph_data, x='Date', y='Energy', title=f"{display_name} Energy Usage Over Time")

    # bar graph
    bar_fig = px.bar(graph_data, x='Date', y='Energy', title=f"{display_name} Energy Usage Over Time")

    # dash components wrapper
    return html.Div([
        html.Div([
            
            dcc.Graph(id='line-graph'),
            dcc.Graph(id='bar-graph')

        ], style={'padding': '20px'})
    ])
