from dash import callback, Input, Output, html, dcc
from pages.startup.startup_layout import images, facts

dash_button_style = {
    'fontSize': '20px',
    'padding': '10px 25px',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'border': 'none',
    'backgroundColor': '#004C97',
    'color': 'white',
    'fontFamily': "'Anton', sans-serif",
    'textDecoration': 'none',
    'display': 'inline-block',
}

@callback(
    Output('image-display', 'style'),
    Output('fact-box', 'children'),
    Input('image-interval', 'n_intervals')
)
def update_image(n):
    image_url = images[n % len(images)] 
    fact_text = facts[n % len(facts)]

    #print(f"Showing image: {image_url} (interval {n})")  # debug 

    style = {
        'height': '100vh',
        'width': '100vw',
        'backgroundImage': f'url({image_url})',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'transition': 'background-image 0.8s ease-in-out',
        'position': 'relative',
        'overflow': 'hidden',
    }

    # fact text + button under it
    fact_box_children = html.Div([
        html.P(fact_text, style={'marginBottom': '30px'}),
        dcc.Link(
            html.Button("Desktop", style=dash_button_style),
            href='/homepage'
        )
        ,
        dcc.Link(
            html.Button("Mobile", style=dash_button_style),
            href='/mobile_homepage'
        )
    ])
    return style, fact_box_children
