import dash
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Output, Input  
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from datetime import datetime as dt, timedelta
import plotly.graph_objects as go

df = pd.read_csv('sorted_file.csv')

df['Processed_Date'] = pd.to_datetime(df['Processed_Date'])

df_long = pd.DataFrame(df)


# Aggregate the data by counting occurrences 
#Converting to wide-format for plotly express
df_aggregated = df_long.groupby(['Processed_Date', 'Ratings']).size().unstack(fill_value=0).reset_index()

# Rename columns for clarity
df_aggregated.columns.name = None  # Remove column name
df_aggregated = df_aggregated.rename(columns={1.0: 'Rating_1', 2.0: 'Rating_2', 3.0: 'Rating_3', 4.0: 'Rating_4', 5.0: 'Rating_5'})

# print(df_aggregated)
df_aggregated = df_aggregated.drop([11,12,13,14])
df_aggregated.reset_index(drop=True, inplace=True)
df_aggregated['Total Votes'] = df_aggregated[['Rating_1','Rating_2',  'Rating_3', 'Rating_4',  'Rating_5']].sum(axis=1)


# print(df_aggregated)

#Drop outliers

app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
    html.H1("Multimodal-Time-Binning"),
#Creates a dropdown list for epochs
html.H3("Choose-Epoch"),
    dcc.Dropdown(id='Epoch',
                 options=[{'label': x , 'value': x}
                          for x in ([1,2,3,4,5,6,7,8,9,10,11,12])],
                 value=6  # default value
                 ),
    dcc.Graph(id='python-graph', figure={}),
    ])
])




@app.callback(
    Output(component_id='python-graph', component_property='figure'),
     [Input(component_id='Epoch', component_property='value')]
)
# callbackfunction
def interactive(epoch_value):
    # global df_aggregated
    end_date = pd.to_datetime(dt.now())
    start_date = pd.to_datetime(end_date - pd.DateOffset(months=epoch_value+2))
    
    new = df_aggregated[(df_aggregated['Processed_Date'] >= start_date) & (df_aggregated['Processed_Date']<= end_date)]
    fig = px.bar(new, x='Processed_Date', y=['Rating_1', 'Rating_2', 'Rating_3', 'Rating_4', 'Rating_5'],
             labels={'Processed_Date': 'Date', 'value': 'Count'},
             title='Rating Counts Over Time',
             barmode='group')   


    return fig
        
    



if __name__ == '__main__':
    app.run_server(debug=True, port=8002)















