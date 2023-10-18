import dash
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Output, Input  
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from datetime import datetime as dt, timedelta

# used in the section callback

# df = pd.read_csv("movies.csv")  

# pandas dataframe ---------------------------------------

df = pd.read_csv('sorted_file.csv')
dates = pd.to_datetime(df['Processed_Date'])
ratings = df['Reviews']

df['Processed_Date'] = pd.to_datetime(df['Processed_Date'])
#----------------------------------------------------------



# Page Layout
app = dash.Dash(__name__)
# Html layout
app.layout = html.Div([
#setting up the headings for the page
#Division for Bar-Graph
	html.Div([
    html.H1("Multimodal-Time-Binning", style={
            'color': 'blue', 'fontSize': 40, 'textAlign': 'center'}),
      html.H1("Aditya", style={
            'color': 'black', 'fontSize': 20, 'textAlign': 'left'}),
     html.H2("Graph-1", style={
            'color': 'red', 'fontSize': 30, 'textAlign': 'center'}),

#Creates a dropdown list
    dcc.Dropdown(id='Epoch',
                 options=[{'label': x , 'value': x}
                          for x in ([1,2,3,4,5,6,7,8,9,10,11,12])],
                 value=6  # default value
                 ),
    dcc.Graph(id='python-graph', figure={}),
   ]),

#Division for Pie Chart
    # html.Div([
        
    #      html.H2("Graph-2", style={
    #         'color': 'red', 'fontSize': 30, 'textAlign': 'center'}),
    #     # dcc.Dropdown(id='Choice2',
    #     #              options=[{'label': x, 'value': x}
    #     #                       for x in (df.Genre.unique())],
    #     #              value='Romance'  # default value
    #     #              ),
    #     dcc.Graph(id='python-graph2', figure={}),
    # ]),


#Division for Histogram
    # html.Div([
    #      html.H2("Graph-3", style={
    #         'color': 'red', 'fontSize': 30, 'textAlign': 'center'}),
    #     # dcc.Dropdown(id='Choice3',
    #     #              options=[{'label': x, 'value': x}
    #     #                       for x in (df.Genre.unique())],
    #     #              value='Romance'  # default value
    #     #              ),
    #     dcc.Graph(id='python-graph3', figure={}),
    # ])
    ])


# callback decorator
@app.callback(
    Output(component_id='python-graph', component_property='figure'),
    Input(component_id='Epoch', component_property='value'),
   
)  
#callbackfunction
def interactive(epoch_value):

    rating_data = df.resample('M', on = 'Processed_Date').count()
    end_date = dt.now()
    start_date = end_date - pd.DateOffset(months=epoch_value)
    filtered_data = rating_data[(rating_data.index >= start_date) & (rating_data.index <= end_date)]
    # print(filtered_data)
    # print('here')
    # filtered_data.head()

    fig = px.bar(data_frame = filtered_data, x = filtered_data.index, y = filtered_data['Ratings'], opacity = 0.5, hover_name = 'Ratings', color = filtered_data.index,
                 color_discrete_map={
     })
    return fig
    
    # plt.figure(figsize = (10,6))
    # plt.plot(rating_data.index, rating_data['Ratings'],marker = 'o', linestyle = ' ')
    # plt.xlabel('Date')
    # plt.ylabel('Number of Ratings')
    # plt.title(f'Rating Over Time')
    # plt.grid(True)
    # plt.show()


    # dff = df[df.Genre == genre_value]
    # fig = px.bar(data_frame=dff, x="Audience score %", y="Worldwide Gross", opacity=0.5,hover_name='Film',
    # 	color='Year',   # if values in column z = 'some_group' and 'some_other_group'
    # color_discrete_map={
        
    
    # })
    # return fig
    
# callback decorator
# @app.callback(
#     Output(component_id='python-graph2', component_property='figure'),
#     Input(component_id='Choice', component_property='value'),
    
# )
#callback function  
# def interactive(genre_value):
# #Create copy of dataframe where genre matches selected genre
#     dff = df[df.Genre == genre_value]
#     fig2 = px.pie(data_frame=dff, names="Film", values="Audience score %")
#     return fig2

# callback decorator
# @app.callback(
#     Output(component_id='python-graph3', component_property='figure'),
#     Input(component_id='Choice', component_property='value'),
# )  

# def interactive(genre_value):
#     dff = df[df.Genre == value_genre]
#     fig3 = px.histogram(data_frame=dff,x='Audience score %')
   
#     return fig3
        
    
    
   


    # fig.update_layout(bargap=0.2)
                


if __name__ == '__main__':
    app.run_server(debug=True, port=8002)















