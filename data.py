import dash 
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc 
import dash_html_components as html

import os
import pprint
import pandas as pd 
import plotly.express as px

from Mongo_class import Mongo



mongo_uri = os.getenv('mongo_uri')
m = Mongo(mongo_uri, 'collatz')
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.Div(id='mongo-datatable', children=[]),

    dcc.Interval(id='interval_db', interval=86400000* 7, n_intervals=0),

    html.Button("save to Mongo Database", id="save-it"),
    html.Button('add Row', id='adding-rows-btn', n_clicks=0),

    html.Div(id="show-graphs", children=[]),
    html.Div(id="placeholder")
])

@app.callback(Output('mongo-datatable', 'children'),
              [Input('interval_db', 'n_intervals')])

def populate_datatable(n_intervals):
    #print(n_intervals)

    df = pd.DataFrame(list(m.find_doc(None)))
    
    df = df.iloc[:,1:]
    print(df.head(20))


    return [
        dash_table.DataTable(
            id='my-table',
            columns=[{
                'name':x,
                'id':x,
            } for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case":"sensitive"},
            sort_action= "native",
            sort_mode="single",
            page_current=0,
            page_size=6,
            style_cell={'textAlign': 'left', 'midWidth': '100px'},
        )
    ]
@app.callback(
    Output('show-graphs', 'children'),
    Input('my-table', 'data')

)

def add_row(data):
    df_graph = pd.DataFrame(data)
    df_serial = pd.DataFrame(list(m.find_doc({'type':'serial'})))
    df_threads = pd.DataFrame(list(m.find_doc({'type':'multithread'})))
    df_process = pd.DataFrame(list(m.find_doc({'type':'multi process'})))

    fig_hist1 = px.line(df_graph, x='range', y='total_time',line_group='type',  color='type')
    fig_serial = px.line(df_serial, x='range', y='total_time')
    #fig_threads = px.line(df_threads, x='range', y='total_time', color='number of threads')
    fig_process = px.line(df_process, x='range', y='total_time', color = 'processes')

    return[
        html.Div(children=[dcc.Graph(figure=fig_hist1)], className='six columns'),
        html.Div(children=[dcc.Graph(figure=fig_serial)], className='six columns'),
        #html.Div(childern=[dcc.Graph(figure=fig_threads)], className='six columns'),
        html.Div(children=[dcc.Graph(figure=fig_process)], className='six columns')
    ]
if __name__ == '__main__':
    app.run_server(debug=True)
