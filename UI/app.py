from dash import Dash

# dash app w multi page enabled
app = Dash(__name__, 
           use_pages=True,
           suppress_callback_exceptions=True)
app.title = "Energy Dashboard"