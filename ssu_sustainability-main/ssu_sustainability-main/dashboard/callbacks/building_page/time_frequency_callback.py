from dash import Input, Output, State, callback
from data.constants import building_timestamp_data

# this callback will change the frequency of time on the graphs based on what is selected by the time frequency dropdown menu

@callback(
    Output('time-range-slider', 'min'),
    Output('time-range-slider', 'max'),
    Output('time-range-slider', 'value'),
    Output('time-range-slider', 'marks'),
    Input('time-frequency-dropdown', 'value'),
    State('url', 'pathname')
)
def update_slider_range(frequency, pathname):

    # get building name from pathname
    building_key = pathname.split("/building/")[-1].replace("_", " ")

    if building_key not in building_timestamp_data:
        return 0, 0, [0, 0], {}

    data = building_timestamp_data[building_key][frequency]
    return (
        data['min_index'],
        data['max_index'],
        [data['min_index'], data['max_index']],
        data['marks']
    )
