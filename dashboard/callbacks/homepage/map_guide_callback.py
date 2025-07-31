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
    Output("filters-highlight", "style"),
    Output("graphs-highlight", "style"),  
    Input("map-guide-btn", "n_clicks"),        
    Input("close-guide-btn", "n_clicks"),
    Input("welcome-close-guide-btn", "n_clicks"),
    Input("guide-prev", "n_clicks"),
    Input("guide-next", "n_clicks"),
    Input("welcome-guide-next", "n_clicks"),
    State("welcome-overlay", "style"),
    State("guide", "style"),
    State("guide-page", "data"),
    State("filters-highlight", "style"),
    State("graphs-highlight", "style"),
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
    current_page,
    filters_style,
    graphs_style,
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    triggered = ctx.triggered[0]['prop_id'].split('.')[0]
    num_pages = len(GUIDE_PAGES)

    # styles
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
        'zIndex': 11000,
    }
    hidden_welcome = {'display': 'none'}

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
        'zIndex': 12000,
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
        'display': 'block',
        'zIndex': 10000,
    }
    hidden_dim = {'display': 'none'}

    filters_style = filters_style.copy() if filters_style else {}
    graphs_style = graphs_style.copy() if graphs_style else {}
    guide_style = guide_style.copy() if guide_style else visible_guide.copy()

    # default hide dim-overlay and reset highlights
    dim_style = hidden_dim
    filters_style.update({'filter': 'none', 'pointerEvents': 'auto', 'zIndex': 1000})
    graphs_style.update({'filter': 'none', 'pointerEvents': 'auto', 'zIndex': 1000})

    # calculate new_page based on triggered input
    if triggered == "map-guide-btn":
        return visible_welcome, hidden_guide, -1, hidden_dim, filters_style, graphs_style

    elif triggered in ["close-guide-btn", "welcome-close-guide-btn"]:
        return hidden_welcome, hidden_guide, current_page, hidden_dim, filters_style, graphs_style

    elif triggered == "guide-prev":
        new_page = max(current_page - 1, 0)
    elif triggered in ["guide-next", "welcome-guide-next"]:
        if current_page == -1:
            new_page = 0
        else:
            new_page = min(current_page + 1, num_pages - 1)
    else:
        new_page = current_page

    # apply dimming logic based on new_page (not current_page)
    if new_page in [0, 1]:
        dim_style = visible_dim

        if new_page == 0:
            filters_style.update({'filter': 'none', 'pointerEvents': 'auto', 'zIndex': 11000})
            graphs_style.update({'filter': 'brightness(0.4)', 'pointerEvents': 'none', 'zIndex': 1000})
        elif new_page == 1:
            graphs_style.update({'filter': 'none', 'pointerEvents': 'auto', 'zIndex': 11000})
            filters_style.update({'filter': 'brightness(0.4)', 'pointerEvents': 'none', 'zIndex': 1000})

    # guide visibility only on pages >= 0
    guide_visibility = visible_guide if new_page >= 0 else hidden_guide
    welcome_visibility = visible_welcome if new_page == -1 else hidden_welcome

    return welcome_visibility, guide_visibility, new_page, dim_style, filters_style, graphs_style


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