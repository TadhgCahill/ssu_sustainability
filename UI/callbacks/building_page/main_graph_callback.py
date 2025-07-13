from dash import Input, Output, State, callback
import plotly.express as px
from data.constants import building_timestamp_data

# this callback allows the user to change the time range slider and time frequency dropdown menu
# to update the line and bar graphs

@callback(
    Output('line-graph', 'figure'),
    Output('bar-graph', 'figure'),
    Input('time-range-slider', 'value'),
    Input('time-frequency-dropdown', 'value'),
    State('url', 'pathname')
)
def update_building_graphs(slider_range, selected_frequency, pathname):
    if not pathname:
        return px.line(title="No Data"), px.bar(title="No Data")

    # convert path to building name 
    building_key = pathname.strip("/").replace("_", " ")

    building_data = building_timestamp_data.get(building_key, {}).get(selected_frequency)
    if not building_data:
        return px.line(title="No Data"), px.bar(title="No Data")

    df = building_data['data']
    start_idx, end_idx = slider_range
    df_filtered = df.iloc[start_idx:end_idx + 1].copy()

    # rename for plots
    df_filtered.columns = ['Date', 'Energy']

    # line graph
    line_fig = px.line(df_filtered, x='Date', y='Energy', title=f"{building_key} {selected_frequency} Energy Usage")

    # bar graph
    bar_fig = px.bar(df_filtered, x='Date', y='Energy', title=f"{building_key} {selected_frequency} Energy Usage")

    for fig in [line_fig, bar_fig]:
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor="#1A1A1A",
            plot_bgcolor="#272936",
            font=dict(color='white'),
            margin=dict(t=40, l=20, r=20, b=20)
        )

    return line_fig, bar_fig
