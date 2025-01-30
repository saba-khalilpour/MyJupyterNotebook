# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
# TASK 1: Add a dropdown list to enable Launch Site selection
# The default select value is for ALL sites
dcc.Dropdown(id='site-dropdown',options=[{'label': 'All Sites', 'value': 'ALL'},], value='ALL', placeholder="Select a Launch Site here", searchable=True),
html.Br(),

# TASK 2: Add a pie chart to show the total successful launches count for all sites
# If a specific launch site was selected, show the Success vs. Failed counts for the site
 html.Div(dcc.Graph(id='success-pie-chart')),
                                
 @app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value')),def update_pie_chart(selected_site):
 if selected_site == 'ALL':
 #Filter data for all sites
df = spacex_df
else:
# Filter data for the selected site
df = spacex_df[spacex_df['Launch Site'] == selected_site]
html.Br(),
# Create a pie chart     
fig = px.pie(df, names='class', title=f'Success Rate for {selected_site}')
return fig

 # TASK 3: Add a slider to select payload range
#dcc.RangeSlider(id='payload-slider',...)
dcc.RangeSlider(
    id='payload-slider',
    min=0, max=10000, step=1000,
    marks={0: '0', 1000: '1K', 2000: '2K', 10000: '10K'},
    value=[0, 10000]  # Default value for payload range
)
 # TASK 4: Add a scatter chart to show the correlation between payload and launch success
 html.Div(dcc.Graph(id='success-payload-scatter-chart')),

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter_plot(selected_site, selected_payload):
    min_payload, max_payload = selected_payload
    if selected_site == 'ALL':
        df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & (spacex_df['Payload Mass (kg)'] <= max_payload)]
    else:
        df = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                       (spacex_df['Payload Mass (kg)'] >= min_payload) & 
                       (spacex_df['Payload Mass (kg)'] <= max_payload)]
    
    fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Success vs Payload for {selected_site}')
    return fig

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()


