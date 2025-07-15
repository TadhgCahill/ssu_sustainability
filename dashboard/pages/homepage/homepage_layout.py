from dash import html, register_page

# layout imports
from pages.homepage.graphs_layout import graphs
from pages.homepage.filters import filters

register_page(__name__, path='/')

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
        
         # filters section of main page
        html.Div(filters, id='filters-sidebar', style={
            'flex' : '1', 
            'padding' : '10px', 
            'backgroundColor' : "#1B1B1B",
            'height' : '97.7vh',
            'overflowY' : 'auto'
            
        }),

        # graphs section of main page
        html.Div(graphs, style={
            'flex' : '4',
            'padding' : '10px', 
            'backgroundColor' : "#20212A", 
            'color' : 'white',
        })

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

