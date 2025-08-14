from dash import html, dcc, register_page

register_page(__name__, path='/', name="Startup")

images = [
    'assets/startup/images/ssu_sign.jpg',
    'assets/startup/images/ssu_sunset.jpg',
    'assets/startup/images/ssu_student_center.jpg',
    'assets/startup/images/beauj_tree.jpg',
    'assets/startup/images/rec_center.jpg',
    'assets/startup/images/beauj_pond.jpg',
    'assets/startup/images/bacon_eggs.jpg',
    'assets/startup/images/gmc_bridge.jpg',
    'assets/startup/images/library_clocktower.jpg',
    'assets/startup/images/gmc_sky.jpg'
]

facts = [
    "Did you know? Sonoma State's solar array supplies around one-third of the campus with clean energy.",
    "Fact: One kWh of energy can power a 50-watt television for 20 hours.",
    "Over 20 percent of all products SSU Culinary Services purchases are from local farmers and producers.",
    "In 2021, the Sustainability Tracking, Assessment & Rating System (STARS), awarded Sonoma State the Silver rating!",
    "The newly renovated Stevenson Hall is the first LEED certified building on campus, meeting standards for responsible and efficient design!",
]

layout = html.Div ([
    html.Link(
        href="https://fonts.googleapis.com/css2?family=Anton&display=swap", 
        rel="stylesheet"
    ),
    dcc.Location(id='url', refresh=True),

    # speed up or slow down startup screen interval here
    dcc.Interval(id='image-interval', interval=10000, n_intervals=0),
    #dcc.Interval(id='image-interval', interval=5000, n_intervals=0),

    html.Div([
        # text box
        html.Div(id='fact-box', style={
            'position': 'absolute',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'backgroundColor': "rgba(11, 47, 131, 0.8)",
            'color': 'white',
            'padding': '50px 100px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'fontSize': '30px',
            'fontFamily': "'Anton', sans-serif",
            'maxWidth': '70%',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.3)'
        }),
    ], id='image-display', style={
        'height': '100vh',
        'width': '100vw',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'transition': 'background-image 0.8s ease-in-out',
        'position': 'relative',  
        'overflow': 'hidden'
    })

])