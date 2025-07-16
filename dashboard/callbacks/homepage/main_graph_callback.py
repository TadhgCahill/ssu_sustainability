from dash import Input, Output, callback
import plotly.express as px
from data.csv_source import df
from data.constants import geo_json_buildings, building_centers
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# this callback updates the three graphs based on the location, unit, and timestamp selected in the filters section

# functions to get building center lon and lat
def get_building_center_lon(name):
    return building_centers.get(name, (None, None))[1]
 
def get_building_center_lat(name):
    return building_centers.get(name, (None, None))[0]

# main callback which updates the three graphs when any of the input ids are changed 
@callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Input('location-filter', 'value'),
    Input('unit-filter', 'value'),
    Input('timestamp-filter', 'start_date'),
    Input('timestamp-filter', 'end_date'),
    Input('map-overlay-type', 'value'),
    Input('map-layer-toggles', 'value')
)
def update_graphs(selected_locations, selected_units, start_date, end_date, overlay_type, map_toggles):
    # convert date str to datetime.date 
    if start_date is not None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date is not None:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # filter dataframe based on filters selected
    filtered_df = df[
        (df['truncated_location'].isin(selected_locations)) & 
        (df['unit'].isin(selected_units)) &
        (df['date_only'] >= start_date) &
        (df['date_only'] <= end_date)
    ]

    if filtered_df.empty:
        print("Filtered DataFrame is empty — returning blank figures.")
        return go.Figure(), go.Figure(), go.Figure()
    
    # group by location and sum up value
    aggregated_df = filtered_df.groupby('truncated_location', as_index=False)['energy_usage'].sum()

    # add column of truncated location name 
    #aggregated_df['truncated_location'] = aggregated_df['location'].apply(truncate_name)

    # add columns for building center lon and lat by building
    aggregated_df['center_lon'] = aggregated_df['truncated_location'].apply(get_building_center_lon)
    aggregated_df['center_lat'] = aggregated_df['truncated_location'].apply(get_building_center_lat)

    # csv for debugging contents of aggregated_df
    aggregated_df.to_csv('temp_agg_df.csv', index=False)

    # map settings checklist variables
    show_outline = 'show_outline' in map_toggles
    show_name = 'show_name' in map_toggles
 
    # update map (plotly graph objects with MapLibre map)
    figure1 = update_figure1(aggregated_df, overlay_type, show_campus_outline=show_outline, show_campus_name=show_name)

    # update plotly bar graph 
    figure2 = update_figure2(aggregated_df)

    # update plotly donut chart 
    figure3 = update_figure3(aggregated_df)


    return figure1, figure2, figure3

def update_figure1(aggregated_df, overlay_type, show_campus_outline=True, show_campus_name=True):

    # coordinates defining campus shape
    campus_polygon = [
        [38.343309, -122.679879],
        [38.343311, -122.674769],
        [38.346074, -122.672685],
        [38.346182, -122.666775],
        [38.336137, -122.666731],
        [38.336032, -122.679787],
        [38.343309, -122.679879]
    ]

    # campus trace
    campus_map_trace = go.Scattermap(
        lat=[pt[0] for pt in campus_polygon],
        lon=[pt[1] for pt in campus_polygon],
        mode='lines',
        fill='toself',
        fillcolor='rgba(0, 110, 255, 0.08)',
        line=dict(color='navy'),
        hovertext='Sonoma State University',
        hoverinfo='text'
    )

    # campus name trace 
    campus_name_trace = go.Scattermap(
        lat=[38.33699181601771], 
        lon=[-122.67480922443565],
        mode='markers+text',
        marker=dict(size=0, opacity=0),  
        text=['Sonoma State University'],
        textposition='middle center',
        textfont=dict(
            color='white',
            size=22,
        ),
        hoverinfo='skip',
        showlegend=False
    )

    # building name markers
    markers_trace = go.Scattermap(
        lon=aggregated_df['center_lon'],
        lat=aggregated_df['center_lat'],
        text=aggregated_df['truncated_location'],
        customdata=aggregated_df['truncated_location'],
        mode='markers+text',
        textposition='top center',  
        textfont=dict(
            color='white',
            size=13,
        ),
        hoverinfo='text',
        marker=dict(color='teal', size=8)
    )

    # list of traces to include in figure
    traces = []

    if overlay_type == 'choropleth':

        # campus choropleth map trace
        choropleth_map_trace = go.Choroplethmap(
            geojson=geo_json_buildings,
            locations=aggregated_df['truncated_location'],
            z=aggregated_df['energy_usage'],
            featureidkey="properties.id",
            colorscale="Aggrnyl",
            marker_opacity=0.7,
            colorbar=dict(
                title="Value",
                tickfont=dict(color='white')  
            ),
            hovertemplate='%{z:.2f} kWh<extra></extra>'  
        )

        traces.append(choropleth_map_trace)
        #figure1 = go.Figure(data=[choropleth_map_trace, campus_map_trace, markers_trace])

    elif overlay_type == 'bubble':

        # normalizing values so unit doesn't affect bubble sizes
        values = aggregated_df['energy_usage']
        min_val = values.min()
        max_val = values.max()

        if max_val > min_val:
            normalized_values = (values - min_val) / (max_val - min_val)
        else:
            normalized_values = np.zeros_like(values) 

        bubble_size = normalized_values * 120 + 30  # scale 0–1 to 30-150 px

        # campus bubble map trace
        bubble_map_trace = go.Scattermap(
            lon=aggregated_df['center_lon'],
            lat=aggregated_df['center_lat'],
            text=aggregated_df['energy_usage'].apply(lambda x: f"{x:.2f} kWh"),
            mode='markers',
            marker=dict(
                size=bubble_size,
                color=aggregated_df['energy_usage'],
                colorscale='Aggrnyl',
                opacity=0.7,
                colorbar=dict(title='Value',
                              tickfont=dict(color='white'),
                )
            ),
            hoverinfo='text'
        )
        #figure1 = go.Figure(data=[bubble_map_trace, campus_map_trace, markers_trace])
        traces.append(bubble_map_trace)

    if show_campus_outline:
        traces.append(campus_map_trace)

    if show_campus_name:
        traces.append(campus_name_trace)

    traces.append(markers_trace)

    figure1 = go.Figure(data=traces)

    figure1.update_layout(
        map=dict(
            style='carto-darkmatter', 
            center=dict(lat=38.340931449672006, lon=-122.67307511912622),  
            zoom=15
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0F2249",  
    )

    return figure1

def update_figure2(aggregated_df):

    figure2 = px.bar(
        aggregated_df,
        x='energy_usage',
        y='truncated_location',
        title='Sum of Energy Consumption by Location',
        labels={'value': 'Sum of Value', 'truncated_location': 'Location'},
        template='plotly_white',
        hover_name='truncated_location',
        color_discrete_sequence=px.colors.sequential.Aggrnyl 
    )

    figure2.update_layout(
        paper_bgcolor="#1A1A1A",
        plot_bgcolor="#272936",
        font=dict(color='white'),
    )

    return figure2

def update_figure3(aggregated_df):

    figure3 = px.pie(
            aggregated_df,
            names='truncated_location',
            values='energy_usage',
            title='Percent of Energy Used by Location',
            hole=0.5,
            hover_name='truncated_location',
            color_discrete_sequence=px.colors.sequential.Aggrnyl 
        )

    # display percentage values and labels
    figure3.update_traces(textinfo='percent+label', rotation=300)

    figure3.update_layout(
        paper_bgcolor="#1A1A1A",
        plot_bgcolor="#272936",
        font=dict(color='white'),
    )

    return figure3

