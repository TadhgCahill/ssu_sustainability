import dash
from dash import Input, Output, State, callback

# this callback opens or closes the map guide

@callback(
    Output("guide", "style"),
    Input("map-guide-btn", "n_clicks"),
    Input("close-guide-btn", "n_clicks"),
    State("guide", "style"),
    prevent_initial_call=True
)
def toggle_guide(map_clicks, close_clicks, current_style):
    context = dash.callback_context

    if not context.triggered:
        raise dash.exceptions.PreventUpdate
    
    triggered_id = context.triggered[0]['prop_id'].split('.')[0]

    visible_style = {
        'position': 'absolute',
        'top': '60px',
        'right': '10px',
        'width': '250px',
        'padding': '15px',
        'backgroundColor': "#3A219F",
        'color': 'white',
        'borderRadius': '8px',
        'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.3)'
    }

    # Define hidden style
    hidden_style = {'display': 'none'}

    if triggered_id == "close-guide-btn":
        return hidden_style

    if triggered_id == "map-guide-btn":
        return visible_style
    
    return current_style
