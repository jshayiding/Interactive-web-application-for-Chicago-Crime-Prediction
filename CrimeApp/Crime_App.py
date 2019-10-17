# package imports
from Utilities import Utilities
from Preprocess_Feather import Preprocess_Feather

# dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# imports
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path
import sys
import feather

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# crime dataframe used by Dash, set in main()
allcrime = None

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


if __name__ == '__main__':
    # preprocess file path
    config = Path('crimeData.feather')

    #does not exist, create .feather
    if not config.is_file():
        print(">>[PREPROCESS} : .feather File not found --> creating crimeData.feather")
        # create feather format for faster loadtime in future
        #### NOTE : USES PASSED PARAMETER FOR CSV FILE ######
        file = sys.argv[1] # file arg
        preprocess = Preprocess_Feather(file)
        preprocess.createFeather()
        print(">>[PREPROCESS} : File created : crimeData.feather")

    # read .feather, compressed dataframe
    allcrime =  feather.read_dataframe('crimeData.feather')


def crimeGraphDescription():
    return html.Div([
        html.H1('Crime Analysis by Year'),
        html.P('The city of Chicago has collected crime data and kept published it for public use.'),
        html.P('What the Crime Pricers team has done is developed an interactive plot where you can select the crime'),
        html.P('types and the year you wish to display'),
        html.Strong(html.P('Directions:')),
        html.P('1. Select crime types from the dropdown field (multiple can be chosen)'),
        html.P('2. Select the year from the slider'),
        html.P('3. Hover over dots on graph to reveal information about the point'),
        html.Br()
    ], style={'text-align': "center"})

def crimeTypes():
    types = []
    for t in Utilities.crimes_list:
        label = str(t).lower()
        types.append({'label': label, 'value': t})

    return types


app.layout = html.Div([
    crimeGraphDescription(),
    html.Center(
        html.Div([
            html.Label('Crime Type'),
            dcc.Dropdown(
                id='crimes-dropdown',
                options=crimeTypes(),
                value=['ASSAULT','BURGLARY','ROBBERY'],
                multi=True),
            html.Label('Select Year'),
            dcc.Slider(
                id='year-slider',
                min=allcrime['year'].min(),
                max=allcrime['year'].max(),
                value=allcrime['year'].min(),
                marks={str(year): str(year) for year in allcrime['year'].unique()}
            ),
            html.Br()], style= {'width': '40%'})
    ),
    dcc.Graph(id='crime-with-slider'), # main scatter plot showing monthly crime spread over year
    html.Div([
        html.Div([
            dcc.Graph(id='crime-bar-graph', style={'width': '500'}),
        ], style={'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='crime-pie-graph', style={'width': '500'})
        ], style={'display': 'inline-block'})
    ],className='row',style={'display' : 'flex'},)

])


@app.callback(
    Output('crime-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('crimes-dropdown', 'value')])
def crime_scatter_figure(selected_year,selected_crimes):
    year_df = allcrime[allcrime.year == selected_year]

    traces = []
    for i in selected_crimes:
        # set xs
        df = year_df[year_df.primary_type == i]
        data = df[['date', 'primary_type']]
        data = data[data.primary_type == i]
        data['date'] = data['date'].map(lambda x: x.month)
        data = data.groupby('date').count()
        ds = df['date'].map(lambda x: x.month).unique()
        ds.sort()

        traces.append(go.Scatter(
            x=ds,
            y=data['primary_type'],
            mode='lines+markers',
            text= i,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    # return figure
    return {
        'data': traces,
        'layout': go.Layout(
            title="Crime by Month",
            xaxis={
                'title' : 'month',
                'type' : 'linear',
                'ticklen' : len(Utilities.months),
                'dtick' : 1
            },
            yaxis={
                'title' : 'crime count',
                'type' : 'linear'
            },
            hovermode='closest'
        )
    }


@app.callback(
    Output('crime-bar-graph', 'figure'),
    [Input('year-slider', 'value'),
     Input('crimes-dropdown', 'value')])
def crime_bar_figure(selected_year,selected_crimes):
    year_df = allcrime[allcrime.year == selected_year]

    x = selected_crimes
    y = []
    for i in selected_crimes:
        crimesCommited = len(year_df[year_df.primary_type == i])
        y.append( crimesCommited )

    data = [go.Bar(
        x=x,
        y=y,
        text=y,
        textposition='auto',
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5),
        ),
        opacity=0.6
    )]

    # return figure
    return {
        'data': data,
        'layout': go.Layout(
            title="Crime Type Distribution",
            xaxis={
                'title': 'Crime Types'
            },
            yaxis={
                'title': 'Count'
            },
        )
    }


@app.callback(
    Output('crime-pie-graph', 'figure'),
    [Input('year-slider', 'value'),
     Input('crimes-dropdown', 'value')])
def crime_pie_figure(selected_year,selected_crimes):
    year_df = allcrime[allcrime.year == selected_year]
    values = []
    for i in selected_crimes:
        df = year_df[year_df.primary_type == i]
        perc = round(len(df) / len(year_df) * 100,0)
        values.append( perc )

    data = [go.Pie(
        hole = 0.4,
        hoverinfo = "label+percent+name",
        labels = selected_crimes,
        name = "Crime by Percent",
        textposition =  "inside",
        values = values
    )]

    layout = go.Layout(
         annotations = [
               {
                   "font": {"size": 20},
                   "showarrow": False,
                   "text": "Breakdown"
               }
           ],
           title = "Selected Crimes Percent Breakdown"
    )


    return {
        'data' : data,
        'layout' : layout
    }


##############################################

# run shiny app
app.run_server(debug=True)
