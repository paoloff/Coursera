# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from PIL import Image


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# Create a dash application
app = dash.Dash(__name__)
values = pd.unique(spacex_df['Launch Site'])
drop_values = ['Relative Outcomes in ' + site_name for site_name in pd.unique(spacex_df['Launch Site'])] 
dics=[{'label': drop_values[i],'value':values[i]} for i in range(len(values))]
dics.insert(0,{'label':'Fraction of Successes per Site','value':'ALL'})

# Image object
pil_image = Image.open("3.png")


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Falcon 9 Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#000D90',
                                               'font-size': 40, }),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(style={'backgroundColor': 'red'}),
                                html.H1('How a Falcon 9 Rocket looks like',
                                        style={'textAlign': 'Left', 'color': '#1C7ECF',
                                               'font-size': 30}),
                                html.Img(src=pil_image, width=1000),
                                html.Br(),
                                html.H1('Select a Pie Chart',
                                        style={'textAlign': 'Left', 'color': '#1C7ECF',
                                               'font-size': 30}),
                                html.Div(dcc.Dropdown(id='site-dropdown',   
                                options=dics,
                                value='ALL',
                                placeholder='Select a Launch Site here',
                                searchable=True)),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.H1('Distribution of Payloads and Outcomes for Different Booster Versions',
                                        style={'textAlign': 'left', 'color': '#1C7ECF',
                                               'font-size': 30}),
                                html.P("Select the Payload range (Kg):", style={'font-size':20}),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',min=0 ,max=10000, step=1000, value=[0, 10000])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([
                                     dbc.Row([
                                    dbc.Col([dcc.Graph(id='success-payload-scatter-chart')])],align='center'
                                     )])
                                ]

)



# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='Outcome', 
        names='Launch Site', 
        title='Fraction of All Successes That Belong to each Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.pie(filtered_df, names='Outcome',title='Relative Outcomes for Specific Site. Red = Success; Blue = Failure')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value"))
def get_scatter_plot(entered_site, payload):
    p1 = payload[0]
    p2 = payload[1]
    data = spacex_df.loc[(spacex_df['Payload Mass (kg)']>p1) & (spacex_df['Payload Mass (kg)']<p2)]
    if entered_site == 'ALL':
        fig = px.scatter(data, x='Payload Mass (kg)', y='Outcome',
                        color="Booster Version", title='All', width=1200)
        return fig
    else:
        data = data[data['Launch Site']==entered_site]
        fig = px.scatter(data, x='Payload Mass (kg)', y='Outcome',
                        color="Booster Version", title='Specific', width=1200)
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
