# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
from collections import defaultdict

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites = [each for each in spacex_df['Launch Site'].unique()]
site_dict = {each:each for each in sites}
site_dict['All'] = 'ALL Sites'

num_good = defaultdict(int)
num_all = defaultdict(int)
site_pct = defaultdict(int)
for i in range(len(spacex_df)):
    site = spacex_df['Launch Site'][i]
    num_good[site] += spacex_df['class'][i]
    num_all[site] += 1
for each in sites:
    site_pct[each] = num_good[each] / num_all[each]
    

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options = site_dict, value = 'All', placeholder = 'Select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min = 0, max = 10000, step = 1000,
                                                marks = {num:str(num) for num in range(0,12500,2500)},
                                                value = [0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback (
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'),
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == "All":
        fig = px.pie( values = num_good.values(), names = num_good.keys(), title = 'Total Success Launches By Site')
        return fig
    else:
        fig = px.pie (values = (num_good[entered_site], num_all[entered_site] - num_good[entered_site] ), names = ['Success', 'Fail'] , title = ' Site Success Pie')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
)
def get_scatter_chart(entered_site):
    if entered_site != "All":
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    else:
        filtered_df = spacex_df
    fig = px.scatter( x= filtered_df['Payload Mass (kg)'], y =filtered_df['class'], color = filtered_df['Booster Version Category'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
