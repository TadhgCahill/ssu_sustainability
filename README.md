## Table of Contents
- [About](#about)
  - [Gallery](#gallery)
      
- [Getting Started](#getting-started)
  - [Clone the Repo](#clone-the-repo)
  - [Conda Environment](#conda-environment)
  - [Running the Program](#running-the-program)
 
- [Components](#components)
  - [Frontend](#frontend)
    - [Frontend Structure](#frontend-structure)
  - [Backend](#backend)
    - [Database](#database)
    - [Data Pipeline](#data-pipeline)      
    
- [License](#license)
  
- [Acknowledgements](#acknowledgements)

## About
Welcome to the SSU Sustainability project! This project is a web application allowing a user to see the gas and/or electric usage of various buildings in Sonoma State University.

### Gallery

Idle Screen with Cycling Facts and Images
<img width="944" height="484" alt="image" src="https://github.com/user-attachments/assets/5c6d6617-67ef-448a-a18f-f36eabbe3e41" />

Guided Tutorial 
<img width="946" height="494" alt="image" src="https://github.com/user-attachments/assets/495e193e-d059-4f71-82c9-ea72086567b8" />

Homepage
<img width="943" height="495" alt="image" src="https://github.com/user-attachments/assets/12629670-ba20-498c-866f-e17408e0aaf6" />

Building Page (Location Specific)
<img width="939" height="496" alt="image" src="https://github.com/user-attachments/assets/ceda1f3d-8f0b-4f77-aaee-6a2cb49271c2" />

## Getting Started

### Clone the Repo
```
git clone <repository url>
```

### Conda Environment

#### Creating Conda Environment
```
# create env
conda create --name conda_ssu_sustainability

# install required packages
conda install dash pandas sqlite sqlalchemy
```

#### Running Conda Environment
```
# activate env command
conda activate conda_ssu_sustainability
```

### Running the Program
```
# go to dashboard directory
cd dashboard

# run program
python index.py
```

## Components

### Frontend
The frontend is built using the Dash Web Framework + Plotly to generate the graphs and maps. You will find all of the frontend components in the "dashboard" folder.

#### Frontend Structure
```
dashboard
│   │   app.py
│   │   index.py
│   │   temp_agg_df.csv
│   │
│   ├───assets
│   │   │   geo-json-buildings.json
│   │   │   info-icon.png
│   │   │   qr_code.png
│   │   │
│   │   └───startup
│   │       └───images
│   ├───callbacks
│   │   ├───building_page
│   │   ├───homepage
│   │   └───startup
│   ├───data
│   │   │   constants.py
│   │   │   csv_source.py
│   │   │   normalized_data4.csv
│   │   │   sql_credentials.py
│   ├───pages
│   │   ├───building_page
│   │   │   │   building_page_layout.py
│   │   │   │   filters.py
│   │   │   │   graphs_layout.py
│   │   ├───homepage
│   │   │   │   filters.py
│   │   │   │   graphs_layout.py
│   │   │   │   homepage_layout.py
│   │   └───startup
│   │       │   startup_layout.py
```

**app.py**
This file is where the dash app is initialized. The app title can be changed here, as well as some flags like "supress callback exceptions." Keep use_pages set to True since this is a mulit page Dash App.

**index.py**
Callbacks will be explained later, but this folder is where you import any callbacks you make. Your callback will NOT be found by Dash's listener if you do not import it in this file. This file is also where the app.layout is defined. 

**assets**
The assets folder is the folder that Dash looks for by default for any STATIC images or files you want to add, like CSS stylesheets, javascript files, images, fonts, etc. 

The file geo-json-buildings.json is how we add new buildings to the map. For example, if in the future meter data was recorded for say, Beaujolais Village, you would add a new entry to this geo-json file like the following:

```
{
            "type" : "Feature",
            "geometry" : {
                "type" : "Polygon",
                "coordinates" : [
                    [
                        [-122.66998890553864, 38.344761408274934],
                        [-122.66890957522975, 38.344761408274934],
                        [-122.66890475679087, 38.34415297659464],
                        [-122.66982026017791, 38.34414163930988],
                        [-122.6697961679835, 38.343676809106],
                        [-122.66943478506757, 38.34367302998642],
                        [-122.66942514818983, 38.34325354648827],
                        [-122.67001299773305, 38.34322709249253],
                        [-122.66998890553864, 38.344761408274934]
                    ]
                ]
            }, 
            "properties" : {
                "id" : "Beaujolais Village",
                "center_lon" : -122.6694231829575, 
                "center_lat" :  38.34395293745609
            }
        },

# note: these coordinates are for the Green Music Center
```

The coordinates can be obtained by going on google maps and right clicking "corners" of the building, and copy the point that pops up. The center lon and lat will be used by code elsewhere to place a clickable "marker" or for building names.

**callbacks**
Dash callbacks are python functions that allow this app to be interactive. Dash listens for changes in component properties, for example if a checkbox is checked or unchecked in the filters section, Dash sees this and automatically runs whatever function we assigned to run. 
This folder contains ALL of the callbacks, separated by folder corresponding to their location on the frontend. There are three main locations as of writing this, startup (the page that cycles images and facts), homepage (the main page with the map), and building page (the page you get to when clicking on a building marker on the map).

The below callback is for the filters section. Based on the units and timestamp start and end dates that the user selects, (by interacting with the elements with ids timestamp-filter or unit-filter), this callback will automatically update the building locations available to the user. This is because we want the user to interact with ONLY the buildings that have data based on their selection. See callbacks/homepage/location_filter_callback.py for the entire code.
```
# example callback

@callback(
    Output('location-filter', 'options'),
    Output('location-filter', 'value'),
    Input('unit-filter', 'value'),
    Input('timestamp-filter', 'start_date'),
    Input('timestamp-filter', 'end_date')
)
def update_location_options(selected_units, start_date, end_date):

     ...

    return options, values
```

**data**
The data folder is the main entrypoint for connecting our web app to the database. The file csv_source.py has our connection to the database, and then constants.py will load all of the possible options for locations, units, timestamp ranges, and building locations from the GeoJSON file. It also loads the options for the building page as well. If you added a building to the GeoJSON file, you would also need to add it as an option in constants.py, so the truncate_name function knows it exists. Changes to the unit options section will also be needed if new units other than Electric and Gas.

**pages**
The pages folder contains the layouts for each of the three different webpages. The majority of this section is going to be html and css. If you wanted to add a button, this is where you will do it and assign the element an "id." This "id" then can be used as an Input(id) for any callbacks you make regarding that button.

For the startup page, there is only one startup_layout.py folder.

The homepage has the majority of the code. Homepage_layout is the "parent" to the homepage code. Here, you will find the title bar, highlights for the guided tutorial, a call to filters and graphs, the welcome mesage, and the bottom border.

Here is the part that has to do with calling filters and graphs. Notice we are importing graphs and filters from graphs_layout.py and filters.py, respectively
```
from dash import html, register_page, dcc

# layout imports
from pages.homepage.graphs_layout import graphs
from pages.homepage.filters import filters

# main homepage
    html.Div([

        html.Div([
            html.Div(children=**filters**)
        ], 
        id='filters-highlight',  
        style={
            ...
        }),

        # graphs section of main page
        html.Div([
            html.Div(**graphs**, 
                id="graphs-section-inner",
                style={
                    ...
                }
            )
        ], id='graphs-highlight', style={
            ...
        }),
```

Filters.py is the filters section you see to the left of the map.

Graphs_layout.py contains three main graphs, graph1 is the map, graph2 is the top right bar graph, and graph3 is the bottom right donut graph.

### Backend

#### Database

#### Data Pipeline

## License

## Acknowledgements
Thanks to Dr. Roya Salek, Dr. Farid Farahmand, and all the contributors!
