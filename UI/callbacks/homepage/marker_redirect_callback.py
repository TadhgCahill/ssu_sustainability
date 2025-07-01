from dash import callback, Output, Input
from dash.exceptions import PreventUpdate

@callback(
    Output('url', 'pathname'),
    Input('graph1', 'clickData'),
    prevent_initial_call=True
)
def redirect_on_marker_click(clickData):
    #print("Clicked:", clickData)
    #raise PreventUpdate

    if not clickData or 'points' not in clickData:
       raise PreventUpdate
    
    building_name = clickData['points'][0]['customdata']
    building_name_underscores = building_name.replace(" ", "_")  # Replace spaces with underscores

    return f"/{building_name_underscores}"