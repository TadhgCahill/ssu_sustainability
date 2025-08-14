from dash import Dash

# dash app w multi page enabled
app = Dash(__name__, 
           use_pages=True,
           suppress_callback_exceptions=True, 
           update_title=False,
           external_scripts=["https://www.googletagmanager.com/gtag/js?id=G-7PJE7B9NP1"])

app.title = "Energy Dashboard"