import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import plotly.plotly as py
import plotly.graph_objs as graph_objs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

#access token for mapbox
mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

#Dict map betwen neighborhood and community
name_map = {'hanson park': 'belmont cragin',
            'edgebrook': 'forest glen',
            'old edgebrook': 'forest glen',
            'south edgebrook': 'forest glen',
            'sauganash': 'forest glen',
            'wildwood': 'forest glen',
            'belmont gardens': 'hermosa',
            'kelvyn park': 'hermosa',
            'lakeview': 'lake view',
            'the loop': 'loop',
            'new east side': 'loop',
            'south loop': 'loop',
            'dearborn park': 'near south side',
            "printer's row": 'near south side',
            'south loop nss': 'near south side',
            'prairie district': 'near south side',
            'little italy': 'near west side',
            'tri-taylor': 'near west side',
            'horner park': 'north center',
            'roscoe village': 'north center',
            'schorsch forest view': 'ohare',
            'south lawndale / little village': 'south lawndale',
            'brainerd': 'washington heights',
            'longwood manor': 'washington heights',
            'princeton park': 'washington heights',
            'east village': 'west town',
            'noble square': 'west town',
            'polish downtown': 'west town',
            'pulaski park': 'west town',
            'smith park': 'west town',
            'ukrainian village': 'west town',
            'wicker park': 'west town'}

#read in geojson file
with open('chicago_communities.geojson') as f:
    geo_f = f.read()
    geojson = json.loads(geo_f)

#get names of all communities in geojson
names = [geojson['features'][k]['properties']['community'].lower() for k in range(len(geojson['features']))]

#get a dictionary of code and name
code_name_dict = {}
for c in geojson['features']:
    code_name_dict[int(c['properties']['area_numbe'])] = c['properties']['community'].lower()

#Read in real estate file
realestate = []
with open('ppsf.csv', encoding='utf-16') as re_file:
    next(re_file)
    reader = csv.reader(re_file, delimiter='\t')

    for row in reader:
        realestate.append(row)

#Duplicate neighborhood 'south loop' because it belongs to both 'loop' and 'near south side'
southloop = []
for row in realestate:
    if row[0].replace('Chicago, IL - ', '').lower() == 'south loop':
        southloop = row.copy()
        break
southloop[0] = 'south loop nss'
realestate.append(southloop)

#Lowercase community names
for row in realestate:
    row[0] = row[0].replace('Chicago, IL - ', '').lower()

#Transform neighborhood name to community name
for row in realestate:
    if row[0] in name_map.keys():
        row[0] = name_map[row[0]]

#Get all community names from real estate file
communities = []
for row in realestate[1:]:
    communities.append(row[0])

#Get communities that exist both in real estate file and in geojson file
duplicate = list(set(communities).intersection(names))
duplicate.sort()

#Get headers
headers = realestate[0]
headers[0] = 'Community'

#Create data frame
re_df = pd.DataFrame(realestate[1:], columns=headers)
re_df = re_df.loc[re_df['Community'].isin(duplicate),:]


#Cast price into float
for i in range(1, len(headers)):
    re_df[headers[i]] = pd.to_numeric(re_df[headers[i]])

#Group by neighborhood and get average price
re_df = re_df.groupby('Community', as_index=False).agg('mean')

#Set index to 'Community' column, prepare for transpose
re_df.set_index('Community')

#Transpose
re_df = re_df.T

#Get new column names, to be community name
cols = re_df.iloc[0]
#Reset df from the 1st price row
re_df = re_df[1:]
#Reset column names
re_df.columns = cols

#Add new column 'year' to be same as index column (now to be month)
re_df['year'] = re_df.index

#Get year array from the df
years = re_df['year'].values

#Trim this array so that only year remains
temp = []
for y in years:
    temp.append(y[-4:])
re_df['year'] = temp

#Cast data back to float
for c in re_df.columns:
    re_df[c] = pd.to_numeric(re_df[c])

#Group by year, then take average price in that year
re_df = re_df.groupby('year', as_index=False).agg('mean')

#Get list of year for year slider
ticks = re_df['year'].values

#Get communities from geojson that in duplicate
features = []
for feature in geojson['features']:
    if feature['properties']['community'].lower() in duplicate:
        features.append(feature)

#Create geojson file that features only communities in duplicate
geo = {'type': 'FeatureCollection', 'features': features}

#Calculate centers of communities as well as get names
geo_longs = []
geo_lats = []
geo_names = []
for k in range(len(geo['features'])):
    neighborhood_coords = np.array(geo['features'][k]['geometry']['coordinates'][0][0])
    m, M = neighborhood_coords[:, 0].min(), neighborhood_coords[:, 0].max()
    geo_longs.append(0.5 * (m + M))
    m, M = neighborhood_coords[:, 1].min(), neighborhood_coords[:, 1].max()
    geo_lats.append(0.5 * (m + M))
    geo_names.append(geo['features'][k]['properties']['community'])

#Read crime data
crime_df = pd.read_csv('crime_community.csv')
#Add community column
coms = []
for c in crime_df['community_area'].values:
    coms.append(code_name_dict[c])
crime_df['name'] = coms
#select only communities in duplicate
crime_df = crime_df.loc[crime_df['name'].isin(duplicate),:]

#Get max price and min price
prices = []
for c in duplicate:
    prices = prices + list(re_df[c].values)
max_price = max(prices)
min_price = min(prices)

#Function to create time series
def create_crime_series(com):
    data = [
        graph_objs.Scatter(
            x=crime_df.loc[crime_df['name']==com, 'year'],
            y=crime_df.loc[crime_df['name']==com, 'count'],
            mode='lines+markers',
            marker={
                'size': 10,
                'opacity': 0.8,
                'color': 'orange',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )
    ]

    layout = graph_objs.Layout(
        xaxis={
            'title': 'Year',
            'type': 'linear'
        },
        yaxis={
            'title': 'Number of Crimes',
            'type': 'linear',
            'range': [0, crime_df.loc[crime_df['name']==com, 'count'].max()]
        },
        annotations=[{
            'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
            'xref': 'paper', 'yref': 'paper', 'showarrow': False,
            'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
            'text': ''
        }],
        margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
        height=350
    )

    fig = dict(data=data, layout=layout)
    return fig

#Function to create real estate time series
def create_re_series(com):
    data = [
        graph_objs.Scatter(
            x=re_df['year'],
            y=re_df[com],
            mode='lines+markers',
            marker={
                'size': 10,
                'opacity': 0.8,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )
    ]

    layout = graph_objs.Layout(
        xaxis={
            'title': 'Year',
            'type': 'linear'
        },
        yaxis={
            'title': 'Price per square foot ($)',
            'type': 'linear',
            'range': [0, re_df[com].max()]
        },
        annotations=[{
            'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
            'xref': 'paper', 'yref': 'paper', 'showarrow': False,
            'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
            'text': ''
        }],
        margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
        height=350
    )

    fig = dict(data=data, layout=layout)
    return fig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    #Header of the page
    html.Div(
        html.H1(children='Chicago Real Estate and Crime'),
        style={'margin': '20px'}
    ),

    #2 slider with their title
    html.Div([
        #Slider for year
        html.Div([
            html.H6('Drag the slider to pick a year between 2012 and 2019'),
            dcc.Slider(
                id='year-slider',
                min=0,
                max=len(ticks)-1,
                value=len(ticks)-1,
                step=1,
                marks={i: str(ticks[i]) for i in range(0,len(ticks))}
            )
        ],
        style={'width': '38%', 'display': 'inline-block'}
        ),

        #Slider for price
        html.Div([
            html.H6(id='range-label'),
            dcc.RangeSlider(
                id='price-slider',
                min=int(min_price),
                max=int(max_price)+1,
                value=[int(min_price), int(max_price)+1],
                step=1,
                marks={
                    int(min_price): str(int(min_price)),
                    (int(max_price)+1): str(int(max_price)+1)
                },
            )
        ],
        style={'width': '45%', 'display': 'inline-block', 'float': 'right', 'padding': '0px 20px 0px 50px'}
        )
    ],
    style={'margin': '30px 50px'}
    ),

    #2 charts with their titles: map and scatter
    html.Div([
        html.Div([
            html.H5(id='heatmap-title', style={'width': '45%', 'display': 'inline-block'}),
            html.H5(id='scatter-title', style={'float': 'right', 'display': 'inline-block', 'width': '45%'}),
        ],
        style={'margin': '20px 50px'}
        ),

        html.Div([
            #Price heat map
            dcc.Graph(
                id='realestate-heatmap',
                figure=dict(
                    data=graph_objs.Data([
                        graph_objs.Scattermapbox(
                            lat=geo_lats,
                            lon=geo_longs,
                            mode='markers',
                            text=geo_names,
                            marker=dict(size=5, color='white', opacity=0.5),
                            hoverinfo='text'
                        )
                    ]),

                    layout=graph_objs.Layout(
                        height=450,
                        autosize=True,
                        hovermode='closest',
                        margin = dict(r=50, l=0, t=0, b=0),
                        mapbox=dict(
                            layers=[],
                            accesstoken=mapbox_access_token,
                            style='light',
                            bearing=0,
                            center=dict(
                                lat=41.845,
                                lon=-87.6231
                            ),
                            pitch=0,
                            zoom=9,
                        )
                    )
                ),
                style={'width': '45%', 'display': 'inline-block'}
            ),

            #scatter plot crime-price
            dcc.Graph(
                id='scatter-plot',
                style={'float': 'right', 'display': 'inline-block', 'width': '50%'}
            )
        ],
        style={'margin': '10px 50px'}
        )
    ]),

    #Crime and real estate trend
    html.Div([
        html.Div([
            html.H5(id='crimetrend-title', style={'width': '45%', 'display': 'inline-block'}),
            html.H5(id='pricetrend-title', style={'float': 'right', 'display': 'inline-block', 'width': '45%'}),
        ],
        style={'margin': '20px 50px'}
        ),

        html.Div([
            #Crime time series
            dcc.Graph(
                id='crime-timeseries',
                style={'width': '45%', 'display': 'inline-block'}
            ),

            #Price time series
            dcc.Graph(
                id='re-timeseries',
                style={'float': 'right', 'display': 'inline-block', 'width': '50%'}
            )
        ],
        style={'margin': '10px 50px'}
        )
    ])
])

#Function to get color from price
def getColor(p):
    viridis = plt.get_cmap('viridis', 256)
    w = max_price - min_price
    val = (p - min_price)/w
    if val == 1:
        return 'rgba' + str(viridis(val - 0.000001))
    else:
        return 'rgba' + str(viridis(val))

#Update heatmap when dragging either the slider
@app.callback(Output('realestate-heatmap', 'figure'),
                [Input('year-slider', 'value'),
                Input('price-slider', 'value')])
def update_heatmap(year, price_range):

    filtered = []
    blackout = []
    ps = {}
    #filter community in price range
    for d in duplicate:
        p = re_df.loc[re_df['year']==ticks[year], d].values[0]
        if (p >= price_range[0]) & (p <= price_range[1]):
            filtered.append(d)
            ps[d] = p
        else:
            blackout.append(d)

    data=graph_objs.Data([
        graph_objs.Scattermapbox(
            lat=geo_lats,
            lon=geo_longs,
            mode='markers',
            text=geo_names,
            marker=dict(size=5, color='white', opacity=0.5),
            hoverinfo='text'
        )
    ])

    lays = []

    #add filtered layers
    if (len(filtered) > 0):
        for feature in geo['features']:
            if feature['properties']['community'].lower() in filtered:
                layer = dict(
                    sourcetype='geojson',
                    source=feature,
                    type='fill',
                    color=getColor(ps[feature['properties']['community'].lower()])
                )
                lays.append(layer)

    #add blackout layers
    if (len(blackout) > 0):
        for feature in geo['features']:
            if feature['properties']['community'].lower() in blackout:
                layer = dict(
                    sourcetype='geojson',
                    source=feature,
                    type='fill',
                    color='rgba(99,99,99,0.3)'
                )
                lays.append(layer)

    layout=graph_objs.Layout(
        height=450,
        autosize=True,
        hovermode='closest',
        margin = dict(r=50, l=0, t=0, b=0),
        mapbox=dict(
            layers=lays,
            accesstoken=mapbox_access_token,
            style='light',
            bearing=0,
            center=dict(
                lat=41.845,
                lon=-87.6231
            ),
            pitch=0,
            zoom=9,
        )
    )

    heatmap = dict(data=data, layout=layout)
    return heatmap

#Update scatter plot when dragging slider or clicking on heatmap
@app.callback(Output('scatter-plot', 'figure'),
                [Input('year-slider', 'value'),
                Input('price-slider', 'value'),
                Input('realestate-heatmap', 'clickData')])
def update_scatter(year, price_range, click):

    filtered = []
    blackout = []
    ps = {}
    #filter community in price range
    for d in duplicate:
        p = re_df.loc[re_df['year']==ticks[year], d].values[0]
        if (p >= price_range[0]) & (p <= price_range[1]):
            filtered.append(d)
            ps[d] = p
        else:
            blackout.append(d)

    #scatter portion for filtered data
    x = []
    y = []
    for d in filtered:
        crime_count = crime_df.loc[(crime_df['year']==(ticks[year]-1)) & (crime_df['name']==d)]['count'].values[0]
        price = re_df.loc[re_df['year']==ticks[year], d].values[0]
        x.append(crime_count)
        y.append(price)

    data = [
        graph_objs.Scatter(
            x=x,
            y=y,
            text=filtered,
            name='inside price range',
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )
    ]

    #scatter portion or blackout data
    x_blackout = []
    y_blackout = []

    for d in blackout:
        crime_count = crime_df.loc[(crime_df['year']==(ticks[year]-1)) & (crime_df['name']==d)]['count'].values[0]
        price = re_df.loc[re_df['year']==ticks[year], d].values[0]
        x_blackout.append(crime_count)
        y_blackout.append(price)

    data.append(
        graph_objs.Scatter(
            x=x_blackout,
            y=y_blackout,
            text=blackout,
            name='outside price range',
            mode='markers',
            marker={
                'size': 15,
                'color': 'rgb(99,99,99)',
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )
    )

    #scatter portion for clicked data
    x_hi = []
    y_hi = []

    if click is not None:
        comm = click['points'][0]['text'].lower()
        crime_count = crime_df.loc[(crime_df['year']==(ticks[year]-1)) & (crime_df['name']==comm)]['count'].values[0]
        price = re_df.loc[re_df['year']==ticks[year], comm].values[0]
        x_hi.append(crime_count)
        y_hi.append(price)

        data.append(
            graph_objs.Scatter(
                x=x_hi,
                y=y_hi,
                text=[comm],
                name=comm,
                mode='markers',
                marker={
                    'size': 15,
                    'color': 'orange',
                    'opacity': 0.7,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )
        )

    layout = graph_objs.Layout(
        xaxis={
            'title': 'Number of Crime',
            'type': 'linear'
        },
        yaxis={
            'title': 'Price per square foot ($)',
            'type': 'linear'
        },
        margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
        height=450,
        hovermode='closest'
    )
    scatter = dict(data=data, layout=layout)
    return scatter

#Update time series when click on map
@app.callback([Output('crime-timeseries', 'figure'),
                Output('re-timeseries', 'figure')],
                [Input('realestate-heatmap', 'clickData')])
def update_series(click):

    if click is not None:
        comm = click['points'][0]['text'].lower()
        crime_line = create_crime_series(comm)
        price_line = create_re_series(comm)
        return crime_line, price_line

    return create_crime_series('albany park'), create_re_series('albany park')

#Update time series title when click on map
@app.callback([Output('crimetrend-title', 'children'),
                Output('pricetrend-title', 'children')],
                [Input('realestate-heatmap', 'clickData')])

def update_series_title(click):
    crime_title = 'Crime Trend in '
    re_title = 'Real Estate Price Trend in '

    if click is not None:
        comm = click['points'][0]['text'].lower()
        crime_title = crime_title + comm.title()
        re_title = re_title + comm.title()
    else:
        crime_title = crime_title + 'albany park'.title()
        re_title = re_title + 'albany park'.title()

    return crime_title, re_title

#Update heatmap and scatter plot titles when drag year slider
@app.callback([Output('heatmap-title', 'children'),
            Output('scatter-title', 'children')],
            [Input('year-slider', 'value')])
def update_title(input):
    map_title = 'Chicago Real Estate in ' + str(ticks[input])
    scatter_title = 'Chicago Real Estate in ' + str(ticks[input]) + ' and Crime in ' + str(ticks[input] - 1)
    return map_title, scatter_title

#Update price range lable when draging price range slider
@app.callback(Output('range-label', 'children'),
                [Input('price-slider', 'value')])
def update_price(input):
    return 'Price between $' + str(input[0]) + ' and $' + str(input[1])

if __name__ == '__main__':
    app.run_server(debug=False)
