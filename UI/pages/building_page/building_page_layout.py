from dash import html, dcc, register_page

# from pages.building_page.graphs_layout import graphs
from pages.building_page.filters import filters_layout
from pages.building_page.graphs_layout import graphs_layout

register_page(__name__, path_template="/<building_name>")
dcc.Location(id='url', refresh=False)

def layout(building_name):
    display_name = building_name.replace("_", " ") 

    layout = html.Div([

        # title bar
        html.H1(f"Energy Usage for {display_name}", style={
                'fontFamily': '"Orbitron", "Segoe UI", sans-serif',
                'textAlign': 'left',
                'marginLeft': '50px',  
                'marginTop': '0px',
                'marginBottom': '10px',
        }),

        # top bar to hold timeframe slider and units checklist
        html.Div([

            # filters section of building page
            html.Div(filters_layout(display_name), id='filters-bar', style={
                'flex' : '1', 
                'padding' : '10px', 
                'backgroundColor' : "#7A0D3E",
            }),

            html.Div(graphs_layout(display_name), id='graphs-section', style={
                'flex': '2',
                'padding': '10px',
                'backgroundColor': "#43A927",
            }),
        ], 
        style={
            'display' : 'flex', 
            'flexDirection' : 'row', 
            'width' : '100%',
            'height' :'100%'
        }),

        # bottom border 
        html.Div(style={
            'height': '50px',                    
            'width': '100%',                    
        }),

    ],
    
    style={
        'backgroundColor': "#274377",  
        'color': 'white',    
        'minHeight': '100vh',
    })


    return layout


