
from dash import html, register_page, dcc

# layout imports
from pages.homepage.graphs_layout import graphs
from pages.homepage.filters import filters

register_page(__name__, path='/homepage', title="Energy Dashboard")

layout = html.Div([

    # title bar
    html.H1("Energy Dashboard", style={
            'fontFamily': '"Orbitron", "Segoe UI", sans-serif',
            'textAlign': 'left',
            'marginLeft': '50px',  
            'marginTop': '0px',
            'marginBottom': '10px',
    }),

    # main homepage
    html.Div([

        html.Div([
            html.Div(children=filters)
        ], 
        id='filters-highlight',  
        style={
            'flex': '1',
            'padding': '10px',
            'backgroundColor': "#1B1B1B",
            'height': '100%',
            'overflowY': 'auto',
            'position': 'relative',
            'transition': 'filter 0.3s ease',  # smooth blur effect
            'zIndex': 9999
        }),

        # graphs section of main page
        html.Div(graphs, 
                id="graphs-section",
                style={
                    'flex' : '4',
                    'padding' : '10px', 
                    'backgroundColor' : "#20212A", 
                    'color' : 'white',
                    'minWidth': '0',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'height': '100%',
                    'overflow' : 'hidden'
                }),

        # map guide information
        html.Div([
            # guide
            html.Label("Guide", style={'color': 'white', 'fontWeight': 'bold', 'fontSize' : '19px'}),
            
            # guide content will be updated by callback
            html.Div(id='guide-content', style={'marginTop': '10px', 'fontSize' : '17px'}),

            # navigation arrows
            html.Div([
                html.Button("←", id='guide-prev', n_clicks=0, disabled=True, style={
                    'marginRight': '10px',
                    'backgroundColor': '#173d6e',
                    'color': 'white',
                    'border': 'none',
                    'cursor': 'pointer'
                }),
                html.Button("→", id='guide-next', n_clicks=0, style={
                    'backgroundColor': '#173d6e',
                    'color': 'white',
                    'border': 'none',
                    'cursor': 'pointer'
                }),
            ], style={'marginTop': '15px'}),

            # 'X' Button
            html.Button("X", id="close-guide-btn", style={
                'right' : '10px',
                'top' : '10px',
                'backgroundColor' : "#173d6e",
                'position' : 'absolute',
                'color' : 'white'
            }),

            # keeping track of page
            dcc.Store(id='guide-page', data=-1)

        ], id = "guide", style={
            'position': 'absolute',
            'bottom': '60px',
            'left': '10px',
            'width': '250px',
            'padding': '15px',
            'backgroundColor': "#5484D2",
            'color': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.3)',
            'display' : 'none'
        })

    ], 
    style={
        'display' : 'flex', 
        'flexDirection' : 'row', 
        'width' : '100%',
        'flex' :'1 1 auto',
        'minHeight' : '0',
        'overflow' : 'hidden'
    }),

    # welcome overlay
    html.Div(
        id='welcome-overlay',
        children=[
            html.Div(
                [
                    html.P(
                        "Welcome to the Energy Usage Dashboard! "
                        "To follow the guided tutorial, use the arrows to navigate. "
                        "To exit, press 'X'.",
                        style={'fontSize': '20px', 'textAlign': 'center', 'color': 'white', 'marginBottom': '20px'}
                    ),
                    html.Div(
                        [
                            html.Button("→", id='welcome-guide-next', n_clicks=0, style={
                                'backgroundColor': '#173d6e',
                                'color': 'white',
                                'border': 'none',
                                'cursor': 'pointer'
                            }),
                            html.Button("X", id='welcome-close-guide-btn', n_clicks=0, style={
                                'marginLeft': '10px',
                                'backgroundColor': '#a83232',
                                'color': 'white',
                                'border': 'none',
                                'cursor': 'pointer',
                                'padding': '0 10px',
                                'fontWeight': 'bold',
                            }),
                        ],
                        style={'display': 'flex', 'justifyContent': 'center', 'gap': '15px'}
                    )
                ],
                style={
                    'backgroundColor': "#405D90",
                    'padding': '30px',
                    'borderRadius': '10px',
                    'maxWidth': '400px',
                    'textAlign': 'center',
                    'boxShadow': '0 0 20px rgba(0,0,0,0.5)'
                }
            )
        ],
        style={
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
    ),

    html.Div(id='dim-overlay', style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '100vw',
        'height': '100vh',
        'backgroundColor': 'rgba(0, 0, 0, 0.7)',  # semi-transparent black
        'pointerEvents': 'none',   # allows clicks to pass through to filters div
        'zIndex': 9998,            # less than filters 
        'display': 'none',         # initially hidden
    }),

    # bottom border 
    html.Div(style={
        'height': '50px',                    
        'width': '100%',                    
    }),
],
style={
    'backgroundColor': "#405D90",  
    'color': 'white',    
    'height': '100vh',
    'display': 'flex', 
    'flexDirection': 'column',
    'margin': '0',
    'padding': '0',
    'overflow': 'hidden',
    'position' : 'relative'
})