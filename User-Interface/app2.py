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

df_aggregated['Average Votes'] = None
df_aggregated['Log2(Total Votes)'] = None
for index, row in df_aggregated.iterrows():
    for rating in (['Rating_1','Rating_2',  'Rating_3', 'Rating_4',  'Rating_5']):
        rating_weight = float(rating[7:])*row[rating]
    if row['Total Votes'] != 0:
        df_aggregated.at[index, 'Average Votes'] = rating_weight / row['Total Votes']
        df_aggregated.at[index, 'Log2(Total Votes)'] = np.log2(row['Total Votes'])
    else:
        df_aggregated.at[index, 'Average Votes'] = 0.0
        df_aggregated.at[index, 'Log2(Total Votes)'] = 0

print(df_aggregated.columns)


# print(df_aggregated)

#Drop outliers

app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
    html.H1("Multimodal-Time-Binning"),
#Plot-1
html.H3("Choose-Epoch"),
    dcc.Dropdown(id='Epoch',
                 options=[{'label': x , 'value': x}
                          for x in ([1,2,3,4,5,6,7,8,9,10,11,12])],
                 value=6  # default value
                 ),
    dcc.Graph(id='python-graph', figure={}),

#Plot-2    
html.H3("Choose Epoch"),
    dcc.Dropdown(id = 'Epoch2',
                  options=[{'label': x , 'value': x}
                          for x in ([1,2,3,4,5,6,7,8,9,10,11,12])],
                 value=6  # default value
                 ),
    dcc.Graph(id='python-graph2', figure={}),

#Plot-3
html.H3("Choose Epoch"),
    dcc.Dropdown(id = 'Epoch3',
                  options=[{'label': x , 'value': x}
                          for x in ([1,2,3,4,5,6,7,8,9,10,11,12])],
                 value=6  # default value
                 ),
    dcc.Graph(id='python-graph3', figure={}),
    ])
])





#---------------------------------------------------------------------------------------------  
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
    fig.add_trace(go.Scatter(x=new['Processed_Date'], y=new['Total Votes'], mode='markers', name='Total Votes'))
    fig.add_trace(px.line(new, x='Processed_Date', y='Total Votes', line_shape="linear").data[0])


    return fig
#---------------------------------------------------------------------------------------------  

#---------------------------------------------------------------------------------------------  
@app.callback(
    Output(component_id='python-graph2', component_property='figure'),
     [Input(component_id='Epoch2', component_property='value')]
)

def interactive(epoch_value):
    # global df
    
    end_date = pd.to_datetime(dt.now())
    start_date = pd.to_datetime(end_date - pd.DateOffset(months=epoch_value+2))
    new= df_aggregated[(df_aggregated['Processed_Date'] >= start_date) & (df_aggregated['Processed_Date']<= end_date)]
    # print(new)
    # print(df_aggregated)
    fig = px.scatter(new, x='Processed_Date', y=['Average Votes','Total Votes'], hover_name="Total Votes",
                 opacity=0.5, labels={'Processed_Date': 'Date'}, color_discrete_map={}, title='Average Vote Over Time',)
    fig.add_trace(px.line(new, x='Processed_Date', y='Average Votes', line_shape="linear").data[0])
    # fig.add_trace(go.Scatter(x=df['X3'], y=df['Y3'], mode='markers', name='Scatter 3'))

    
    # fig.add_trace(px.line(new, x='Month', y='Total Votes', line_shape="linear" ).data[0])


    fig.update_traces(marker=dict(size=12))
    return fig
#--------------------------------------------------------------------------------------------- 

#---------------------------------------------------------------------------------------------  
@app.callback(
    Output(component_id='python-graph3', component_property='figure'),
     [Input(component_id='Epoch3', component_property='value')]
)

def interactive(epoch_value):
    # global df
    
    end_date = pd.to_datetime(dt.now())
    start_date = pd.to_datetime(end_date - pd.DateOffset(months=epoch_value+2))
    new= df_aggregated[(df_aggregated['Processed_Date'] >= start_date) & (df_aggregated['Processed_Date']<= end_date)]
    
    # print(df_aggregated)
    fig = px.scatter(new, x='Processed_Date', y=['Average Votes'], hover_name="Total Votes",
                 opacity=0.5, labels={'Processed_Date': 'Date'}, color_discrete_map={}, title='Average Vote Over Time')
    line_trace = px.line(new, x='Processed_Date', y='Average Votes', line_shape="linear").data[0]
    line_trace['line']['color'] = 'red'  # Set the line color to red
    fig.add_trace(line_trace)
    
    fig.add_trace(go.Scatter(x=new['Processed_Date'], y=new['Log2(Total Votes)'], mode='markers', name='Log(Total Votes)'))
    line_trace = px.line(new, x='Processed_Date', y='Log2(Total Votes)', line_shape="linear").data[0]
    line_trace['line']['color'] = 'blue'  # Set the line color to red
    fig.add_trace(line_trace)
    

    # fig.add_trace(go.Scatter(x=df['X3'], y=df['Y3'], mode='markers', name='Scatter 3'))

    
    # fig.add_trace(px.line(new, x='Month', y='Total Votes', line_shape="linear" ).data[0])


    fig.update_traces(marker=dict(size=12))
    return fig
#--------------------------------------------------------------------------------------------- 
        
    



if __name__ == '__main__':
    app.run_server(debug=True, port=8002)















