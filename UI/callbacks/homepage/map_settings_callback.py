from dash import Input, Output, State, callback

# this callback opens or closes the map settings mini sidebar

@callback(
    Output("sidebar", "style"),
    Output("map-sidebar-btn", "style"),
    Input("map-sidebar-btn", "n_clicks"),
    State("sidebar", "style"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, sidebar_style):
    base_sidebar_style = {
        'position': 'absolute',
        'top': '80px',
        #'left': '180px',
        'padding': '10px',
        'backgroundColor': "#353539",
        'overflow': 'hidden',
        'transition': 'width 0.3s ease',
        'zIndex' : 1000
    }

    base_button_style = {
        'position': 'absolute',
        'top': '10px',
        'height': '40px',
        'backgroundColor': "#2a3f5c",
        'color': 'white',
        'cursor': 'pointer',
        'boxShadow': '0 2px 6px rgba(0,0,0,0.3)',
        'zIndex': 1100,
        'transition': 'left 0.3s ease',
    }

    if n_clicks is None or n_clicks % 2 == 1:
        # Sidebar open
        sidebar_style = {
            **base_sidebar_style,
            'width': '200px',
            'padding': '10px',
            'opacity': '1',
        }
        button_style = {
            **base_button_style,
            'left': '220px'
        }
   
    else:
        # Sidebar closed
        sidebar_style = {
            **base_sidebar_style,
            'width': '0px',
            'padding': '0px',
            'opacity': '0',
        }
        button_style = {
            **base_button_style,
            'left': '10px'
        }
  

    return sidebar_style, button_style
