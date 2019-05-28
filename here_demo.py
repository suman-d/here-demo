import dash
import yaml
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import os 
from dash.dependencies import State, Input, Output
from geopy.geocoders import Here


def get_header():
    header = html.Div([

        html.Div([
            html.H1(
                'HERE GeoCoder Demo')
        ], className="twelve columns padded",
           style={'text-align': 'center', 'margin-bottom': '15px', 'color': '#DC143C'})
        ], className="row gs-header gs-text-header")
    return header

def get_title(t):
    header = html.Div([

        html.Div([
            html.H2(
                '{}'.format(t))
        ], className="twelve columns padded",
           style={'text-align': 'center', 'margin-bottom': '15px', 'color': '#ffffff', 'backgroundColor': '#DC143C' })
        ], className="row gs-header gs-text-header")
    return header

def get_lat_lon(address):
    global APP_ID_HERE, APP_CODE_HERE

    geocoder = Here(APP_ID_HERE, APP_CODE_HERE)
    result = geocoder.geocode(address)

    point = result.point

    return point


# Reading the config file for the APP_ID and APP_CODE
pwd = os.getcwd()
config = pwd + "/config.yml"
with open(config, 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

APP_ID_HERE = cfg["here"]["api_id"]
APP_CODE_HERE = cfg["here"]["app_code"]

# Intializing a global variable for the address to be searched 
test_address = ""

# Starting the Web Application
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
                        [get_header(),
                        html.Div([
                                    html.H3(
                                    "Enter the address",
                                    className=" two columns",
                                    style={
                                        "textAlign": "center",
                                        "width": "20%",
                                        "align-items": "center",
                                        'display': 'inline-block'
                                        },            
                                    ), 
                                    dcc.Input(id='location-text', type='text', value='', 
                                            style={
                                            "display": "flex",
                                            "justify-content": "center",
                                            "align-items": "center",
                                            'display': 'inline-block',
                                            "width": "60%",
                                        }),           
                                    daq.StopButton(
                                        id="submit-button",
                                        buttonText="Find",
                                        style={
                                            "display": "flex",
                                            "justify-content": "center",
                                            "align-items": "center",
                                            "width": "100%",
                                        },
                                        ),
                                    html.H3(id='output-submit', 
                                                style={
                                                    "textAlign": "center",
                                                    "width": "100%",
                                                    "align-items": "flex-start",
                                                    "color": "#DC143C"
                                                    }), 
                                    get_title("Latitude"),
                                    html.H4(
                                        id='output-latitude',
                                        style={
                                            "textAlign": "center",
                                            "width": "100%",
                                            "align-items": "center",
                                            #'display': 'inline-block'
                                            },            
                                    ),
                                    get_title("Longitude"),
                                    html.H4(
                                        id='output-longitude',
                                        style={
                                            "textAlign": "center",
                                            "width": "100%",
                                            "align-items": "center",
                                            #'display': 'inline-block'
                                            },            
                                    )                                    ],
                                            
                            style={
                                    "padding": "10px 10px 10px 10px",
                                    "marginLeft": "auto",
                                    "marginRight": "auto",
                                    "width": "1180px",
                                    "boxShadow": "0px 5px 5px 5px rgba(204,204,204,204)",
                                }), 
                        ]
                     )

@app.callback([Output('output-submit', 'children'),
               Output('output-latitude', 'children'),
               Output('output-longitude', 'children')], 
              [Input('submit-button', 'n_clicks')],
              [State('location-text', 'value')],
              )
def update_output(clicks, input_value):
    global test_address
    if clicks is not None:
        test_address = input_value
        msg = "The Location you have entered is: {}".format(test_address)

        # Fetching the Longitude and Latitude 
        point = get_lat_lon(test_address)
        lon = point.longitude
        lat = point.latitude

        lon_msg = "Longitude is {}".format(lon)
        lat_msg = "Latitude is {}".format(lat)
        
        return [msg, lat, lon]
    else:
        return ["", "Yet to enter an address", "Yet to enter an address"]

# Start the webapp 
app.run_server(host='0.0.0.0', debug=True)




                   

