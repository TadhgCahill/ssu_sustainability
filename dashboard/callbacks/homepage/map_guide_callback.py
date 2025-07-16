import dash
from dash import Output, Input, State, callback, html

GUIDE_PAGES = [
    "Welcome to the energy usage dashboard for Sonoma State University!",
    "Filter the map by location, unit, and timeframe using the left sidebar.",
    "Use 'Map Settings' to toggle overlays between Choropleth and Bubble modes, and change the visibility of layers on the map",
    "Hover over buildings to view the exact energy usage for that building.",
    "Click on a building marker (teal), to view a specific building's energy usage breakdown.",
    "Enjoy!"
]

# callback to navigate guide pages with arrows
@callback(
    Output("guide", "style"),
    Output("guide-page", "data"),
    Input("map-guide-btn", "n_clicks"),
    Input("close-guide-btn", "n_clicks"),
    Input("guide-prev", "n_clicks"),
    Input("guide-next", "n_clicks"),
    State("guide", "style"),
    State("guide-page", "data"),
    prevent_initial_call=True
)
def control_guide(open_clicks, close_clicks, prev_clicks, next_clicks, current_style, current_page):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    triggered = ctx.triggered[0]['prop_id'].split('.')[0]

    visible_style = {
        'position': 'absolute',
        'top': '60px',
        'right': '10px',
        'width': '250px',
        'padding': '15px',
        'backgroundColor': "#5484D2",
        'color': 'white',
        'borderRadius': '8px',
        'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.3)'
    }
    hidden_style = {'display': 'none'}

    num_pages = len(GUIDE_PAGES)

    if triggered == "map-guide-btn":
        return visible_style, 0
    elif triggered == "close-guide-btn":
        return hidden_style, current_page
    elif triggered == "guide-prev":
        return current_style, max(current_page - 1, 0)
    elif triggered == "guide-next":
        return current_style, min(current_page + 1, num_pages - 1)

    return current_style, current_page

# callback to display content
@callback(
    Output('guide-content', 'children'),
    Input('guide-page', 'data')
)
def display_guide_page(page_index):
    return html.P(GUIDE_PAGES[page_index], style={'marginTop': '10px'})