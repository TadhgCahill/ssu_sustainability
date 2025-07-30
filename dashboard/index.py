from app import app

# homepage callbacks
import callbacks.homepage.main_graph_callback
import callbacks.homepage.map_settings_callback
import callbacks.homepage.location_filter_callback
import callbacks.homepage.marker_redirect_callback
import callbacks.homepage.map_guide_callback
import callbacks.homepage.collapse_graphs_callback

# building page callbacks
import callbacks.building_page.time_frequency_callback
import callbacks.building_page.main_graph_callback

# page startup callback
import callbacks.startup.cycle_image_callback

from dash import html, dcc, page_container

#app.layout = layout

app.layout = html.Div([
    dcc.Location(id='url'),
    page_container  
])

if __name__ == '__main__':
    app.run(debug=True)