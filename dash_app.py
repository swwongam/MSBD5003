#!/usr/bin/env python
# coding: utf-8

# In[2]:

import os
import dash
from dash import Dash, html, dash_table, dcc, callback
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


# In[41]:


ptype = pd.read_csv('data/dash_pie_top10.csv', index_col = 0)
community = pd.read_csv('data/dash_community.csv', index_col = 0)
years = sorted(list(ptype['Year'].unique()))

# ### Web App
load_figure_template("darkly")
# In[71]:


app_name = 'Crime-Chicago'
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = 'Chicago Crime Analysis'


# In[72]:


app.layout = html.Div([
    html.H1(children='Chicago Crime Analysis', style={'textAlign': 'center'}),
    html.Hr(),
    # dcc.Dropdown(id = 'select_year',
    #             options = [
    #                 {'label':'2007', "value":2007},
    #                 {'label':'2008', "value":2008},
    #                 {'label':'2009', "value":2009}
    #             ], value = 2007, multi=False, clearable=False, style={"width":"50%"}), 
    dcc.Slider(min = years[0], max = years[-1], step = 1, value = years[0], id = "select_year", marks={str(x):x for x in years}),
    html.Div(children = 
             [dcc.Graph(id = 'pie_chart', style={'display': 'inline-block', 'textAlign': 'center', 'width': '50%', 'height': '100%'}), 
              dcc.Graph(id = 'community_chart', style={'display': 'inline-block', 'textAlign': 'center', 'width': '50%', 'height': '50%'})])
])

# Pie chart
@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    [Input(component_id='select_year', component_property='value')]
)

def update_graph(select_year):
    fig = px.pie(ptype[ptype['Year'] == int(select_year)].sort_values("count", ascending = False).iloc[:10], values='count', names="Primary Type", title='Top 10 Crime Type', color_discrete_sequence=px.colors.sequential.RdBu)
    return (fig)

# Community chart
@app.callback(
    Output(component_id='community_chart', component_property='figure'),
    [Input(component_id='select_year', component_property='value')]
)

def update_graph(select_year):
    comm_df = community[community['Year'] == int(select_year)].dropna()
    fig = px.treemap(comm_df, path=['COMMUNITY'], values=comm_df['count'], height=700, title='Crime in Chicago by Community', color_discrete_sequence = px.colors.sequential.RdBu)
    fig.data[0].textinfo = 'label+text+value'

    return (fig)


# In[73]:


if __name__ == '__main__':
    app.run_server()


# In[ ]:




