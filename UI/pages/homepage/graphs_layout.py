from dash import html, dcc

# empty placeholder graphs
graph1 = dcc.Graph(id='graph1', style={'height': '100%', 'width' : '100%', 'maxWidth': '100%'}, config={'responsive': True})
graph2 = dcc.Graph(id='graph2', style={'height': '100%', 'width' : '100%', 'maxWidth': '100%'}, config={'responsive': True})
graph3 = dcc.Graph(id='graph3', style={'height': '100%', 'width' : '100%', 'maxWidth': '100%'}, config={'responsive': True})


#graph2 = dcc.Graph(id='graph2')
#graph3 = dcc.Graph(id='graph3')

graphs = html.Div([

    # graph 1 
    html.Div([

        # map settings sidebar information
        html.Div([
            html.Label("Map Overlay Type"),
            dcc.RadioItems(
                id='map-overlay-type',
                options=[
                    {'label': 'Choropleth', 'value': 'choropleth' },
                    {'label': 'Bubble', 'value': 'bubble'}
                ],
                value='choropleth',
                labelStyle={'display' : 'block'},
                style={'marginBottom': '10px'}
            )
        ], id="sidebar", style={
            'position' : 'relative',
            'width': '0px', 
            'padding': '0px',
            'opacity': '0',
            'backgroundColor' : "#242430"
        }),

        # map settings button and graph1 
        html.Div([
        html.Button("Map Settings", id="map-sidebar-btn", n_clicks=0, style={
            'position': 'absolute',
            'top': '10px',
            'left': '10px',
            'height': '40px',
            'backgroundColor': "#2a3f5c",
            'color': 'white',
            'cursor': 'pointer',
            'boxShadow': '0 2px 6px rgba(0,0,0,0.3)',
            'zIndex': '10'
        }),
        graph1
        ], style={
            'position': 'relative',
            'flex': 1,
            'minWidth': 0
        })

    ], style={
        'gridArea': 'graph1',
        'display': 'flex',
        'flexDirection': 'row',
        'gap': '10px'
    }),
    

    # graph 2
    html.Div(
        html.Div(graph2, style={'height': '100%'}),
        style={'gridArea': 'graph2',
               'height' : '100%'}
    ),

    # graph 3
    html.Div(
        html.Div(graph3, style={'height': '100%'} ),
        style={'gridArea': 'graph3',
               'height' : '100%'}
    ),
], style={
    'display': 'grid',
    'gridTemplateColumns': '2fr 1fr',
    'gridTemplateRows': '1fr 1fr',
    'gridTemplateAreas': '''
        "graph1 graph2"
        "graph1 graph3"
    ''',
    'gap': '10px',
    'height' : '100%'

})
