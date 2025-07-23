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
            ),

            html.Label("Map Layers", style={'color' : 'white', 'marginTop' : '15px'}),
            dcc.Checklist(
                id='map-layer-toggles',
                options=[{'label': 'Campus Outline', 'value': 'show_outline'},
                         {'label' : 'Campus Name', 'value' : 'show_name'}],
                value=['show_outline', 'show_name'],
                style={'color': 'white'},
                labelStyle={'display' : 'block'}
            )
        ], id="sidebar", style={
            'position' : 'absolute',
            'width': '0px', 
            'padding': '0px',
            'opacity': '0',
            'backgroundColor' : "#242430"
        }),

        # map container 
        html.Div([

            # map settings button
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

            # guide button
            html.Button(
                html.Img(src='/assets/info-icon.png', style={'height': '24px', 'width': '24px'}),
                id="map-guide-btn", n_clicks=0, style={
                'position' : 'absolute',
                'bottom' : '21px',
                'left' : '0px',
                'height' : '40px',
                'width' : '40px',
                'padding' : '0',
                'cursor' : 'pointer', 
                'zIndex': '10',
                'border': 'none',
                'background': 'none',
                'boxShadow': 'none',
            }),
            
            # map
            html.Div([
                graph1
            ], style={
                'flex': '1',
                'minHeight': 0,
                'minWidth': 0,
                'display': 'flex',
                'postion' : 'relative'
            }),

            # map guide information
            html.Div([
                # guide
                html.Label("Guide", style={'color': 'white', 'fontWeight': 'bold', 'fontSize' : '19px'}),
                
                # guide content will be updated by callback
                html.Div(id='guide-content', style={'marginTop': '10px', 'fontSize' : '17px'}),

                # navigation arrows
                html.Div([
                    html.Button("←", id='guide-prev', n_clicks=0, style={
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
                dcc.Store(id='guide-page', data=0)

            ], id = "guide", style={
                'position': 'absolute',
                'bottom': '60px',
                'left': '10px',
                'width': '250px',
                'padding': '15px',
                'backgroundColor': "#5484D2",
                'color': 'white',
                'borderRadius': '8px',
                'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.3)'
            })

        ], style={
            'position': 'relative',
            'flex': 1,
            'minHeight' : 0,
            'minWidth': 0,
            'height': '100%',      
            'display': 'flex',     
            'flexDirection': 'column'
        })

    ], id='main-map', style={
        'flex': '1 1 auto', 
        'padding': '10px',
        'backgroundColor': "#61C81D",
        'color': 'white',
        'minWidth': '0', 
        'display': 'flex',
        'flexDirection': 'column',
        'height' : '100%',
        'minHeight' : '0'
    }),
    
    # collapsible sidebar container for graph2 and graph3
    html.Div([

        # graph2 + graph3 in column
        html.Div([
                html.Div(graph2, style={'height': '100%'}),
                html.Div(graph3, style={'height': '100%'})
        ], id='sidebar-graphs-inner', style={
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '10px',
            'width': '100%',
            'height' : '100%'
        }),

        # hidden store to track open/close state
        dcc.Store(id='collapse-state', data=False)

    ], id='sidebar-wrapper', style={
        'flex': '0 0 300px',  
        'padding': '10px',
        'backgroundColor': '#f8f9fa',
        'position': 'relative',
        'height': '100%',
        'overflow': 'hidden',
        'transition': 'flex-basis 0.3s ease',
        'minWidth': '0'
    }),

    # toggle collapse button
    html.Button("⮞", id='collapse-button', n_clicks=1, style={})

], style={
    'display': 'flex',
    'flexDirection': 'row',
    'height': '100%',
    'width': '100%',
    'position': 'relative',
})
