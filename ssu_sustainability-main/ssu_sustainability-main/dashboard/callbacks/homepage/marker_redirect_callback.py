from dash import callback, Output, Input
from dash.exceptions import PreventUpdate

# this callback redirects a user to a seprate url when they click on the marker for a specific building on the map

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
    
    point = clickData['points'][0]

    # check if customdata exists
    if 'customdata' not in point or point['customdata'] is None:
        raise PreventUpdate
    
    building_name = clickData['points'][0]['customdata']
    building_name_underscores = building_name.replace(" ", "_")  # change spaces with underscores

    return f"/building/{building_name_underscores}"