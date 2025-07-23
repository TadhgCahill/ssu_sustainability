from dash import callback, Input, Output, State

@callback(
    Output('sidebar-wrapper', 'style'),
    Output('collapse-button', 'children'),
    Output('collapse-button', 'style'),
    Input('collapse-state', 'data'),
)
def update_sidebar_style(is_collapsed):
    base_style = {
        'padding': '10px',
        'backgroundColor': '#2a3f5c',
        'position': 'relative',
        'height': '100%',
        'overflow': 'hidden',
        'transition': 'flex-basis 0.3s ease',
        'minWidth': '0',  
        'flexShrink': 0
    }

    base_button_style = {
        'height': '30px',
        'width': '30px',
        'borderRadius': '0 5px 5px 0',
        'backgroundColor': '#173d6e',
        'color': 'white',
        'border': 'none',
        'cursor': 'pointer',
        'boxShadow': '2px 2px 6px rgba(0,0,0,0.2)',
        'position': 'absolute',
        'top': '10px',
        'zIndex': '1', 
        'transition': 'right 0.3s ease',
    }

    if is_collapsed:
        return (
            {
                **base_style,
                'flex': '0 0 0px',  
                'padding': '0px',   
            },
            "⮜",
            {
                **base_button_style,
                'right': '10px'  # shift button to far right
            }
        )
    else:
        return (
            {
                **base_style,
                'flex': '0 0 300px',  
                'padding': '10px'
            },
            "⮞",
            {
                **base_button_style,
                'right': '310px'  # align with open sidebar
            }
        )

@callback(
    Output('collapse-state', 'data'),
    Input('collapse-button', 'n_clicks'),
    State('collapse-state', 'data'),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, current_state):
    return not current_state
