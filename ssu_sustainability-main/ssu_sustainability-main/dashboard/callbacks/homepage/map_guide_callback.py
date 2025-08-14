import dash
from dash import Output, Input, State, callback, html

GUIDE_PAGES = [
    "This is the filters section. You may use it to toggle building visibility, change the unit of energy displayed, and alter the timeframe of energy usage occurred.",
    "GRAPHS",
    "",
    "Enjoy!"
]

# callback to navigate guide pages with arrows
@callback(
    Output("welcome-overlay", "style"),
    Output("guide", "style"),
    Output("guide-page", "data"),
    Output("dim-overlay", "style"),
    Input("map-guide-btn", "n_clicks"),
    Input("close-guide-btn", "n_clicks"),
    Input("welcome-close-guide-btn", "n_clicks"),
    Input("guide-prev", "n_clicks"),
    Input("guide-next", "n_clicks"),
    Input("welcome-guide-next", "n_clicks"),
    State("welcome-overlay", "style"),
    State("guide", "style"),
    State("guide-page", "data"),
    prevent_initial_call=True
)

def control_guide(
    map_guide_btn_clicks,
    close_guide_btn_clicks,
    welcome_close_guide_btn_clicks,
    guide_prev_clicks,
    guide_next_clicks,
    welcome_guide_next_clicks,
    welcome_style,
    guide_style,
    current_page
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    triggered = ctx.triggered[0]['prop_id'].split('.')[0]
    num_pages = len(GUIDE_PAGES)

    # style for darkened background behind welcome guide
    visible_welcome = {
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '100vw',
        'height': '100vh',
        'backgroundColor': 'rgba(0, 0, 0, 0.7)',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'zIndex': 9999,
    }
    hidden_welcome = {'display': 'none'}

    # style for guide box visibility
    visible_guide = {
        'position': 'absolute',
        'bottom': '60px',
        'left': '10px',
        'width': '250px',
        'padding': '15px',
        'backgroundColor': "#405D90",
        'color': 'white',
        'borderRadius': '8px',
        'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.3)',
        'display': 'block',
        'zIndex': 10000,
    }
    hidden_guide = {'display': 'none'}

    visible_dim = {
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '100vw',
        'height': '100vh',
        'backgroundColor': 'rgba(0, 0, 0, 0.7)',
        'pointerEvents': 'auto',
        'zIndex': 9998,
        'display': 'block',
    }
    hidden_dim = {'display': 'none'}

    if triggered == "map-guide-btn":

        # hide guide sidebar, reset page to -1
        # show dim overlay as well to darken background
        return visible_welcome, hidden_guide, -1, hidden_dim

    elif triggered in ["close-guide-btn", "welcome-close-guide-btn"]:

        # closed guide or welcome, hide all overlays and dimming
        return hidden_welcome, hidden_guide, current_page, hidden_dim

    elif triggered == "guide-prev":

        new_page = max(current_page - 1, 0)
        # show dim overlay only if on page 0 (filters)
        return hidden_welcome, visible_guide, new_page, visible_dim if new_page == 0 else hidden_dim

    elif triggered in ["guide-next", "welcome-guide-next"]:

        if current_page == -1:
            # moving from welcome to first guide page (filters)
            return hidden_welcome, visible_guide, 0, visible_dim
        new_page = min(current_page + 1, num_pages - 1)
        return hidden_welcome, visible_guide, new_page, visible_dim if new_page == 0 else hidden_dim

    # fallback keep existing styles, show dim overlay if current page is filters
    return welcome_style, guide_style, current_page, visible_dim if current_page == 0 else hidden_dim


# callback to display content
@callback(
    Output('guide-content', 'children'),
    Input('guide-page', 'data')
)
def display_guide_page(page_index):
    if page_index == -1:
        return "" 
    return html.P(GUIDE_PAGES[page_index], style={'marginTop': '10px'})

@callback(
    Output('guide-prev', 'disabled'),
    Input('guide-page', 'data')
)
def disable_back_button(page_index):
    return page_index <= 0