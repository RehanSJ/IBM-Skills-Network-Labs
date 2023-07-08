#!/usr/bin/env python
# coding: utf-8

# # **Build a Dashboard Application with Plotly Dash**

# In[ ]:


# Open a new terminal, by clicking on the menu bar and selecting Terminal->New Terminal.
# For this project open an new File and name it: "spacex_dash.py"


# In[ ]:


# Install python packages required to run the application.
# Copy and paste the below command to the terminal.

python3.8 -m pip install pandas dash

# Run the following wget command line in the terminal to download dataset as spacex_launch_dash.csv
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
# Download a skeleton Dash app to be completed in this lab (in the terminal):
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
# Test the skeleton app by running the following command in the terminal:
python3.8 spacex_dash_app.py
# In the left Navigation Pane click on Others and click Launch Application option under it.
# Enter the application port number as 8050. Click Your Application.
# Refer back to IBM DS Module 10 Notes Subsection "An Issue Which I Ran Into Using Ploty Dash, Resolution:" If you're running
# into issues with persistant x-axis and y-axis on the launched application.


# ## Task 1: Add a Launch Site Drop-down Input Component

# In[ ]:


# As such, we will need a dropdown menu to let us select different launch sites.
# Find and complete a commented dcc.Dropdown(id='site-dropdown',...) input with following attributes:
# id attribute with value site-dropdown
# options attribute is a list of dict-like option objects (with label and value attributes). You can set
# the label and value all to be the launch site names in the spacex_df
# and you need to include the default All option. e.g.,
  options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'site1'}, ...]
# value attribute with default dropdown value to be ALL meaning all sites are selected placeholder attribute to show
# a text description about this input area such as Select a Launch Site here searchable attribute to be True so we can enter keywords to search launch sites
# Here is an example of dcc.Dropdown:


  dcc.Dropdown(id='id',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'site1', 'value': 'site1'},
                ],
                value='ALL',
                placeholder="place holder here",
                searchable=True
                ),


# ## Task 2: Add a callback function to render success-pie-chart based on selected site dropdown

# In[ ]:


# The general idea of this callback function is to get the selected launch site from site-dropdown and render
# a pie chart visualizing launch success counts.
# Dash callback function is a type of Python function which will be automatically called by
# Dash whenever receiving an input component updates, such as a click or dropdown selecting event.
# Let’s add a callback function in spacex_dash_app.py including the following application logic:
# Input is set to be the site-dropdown dropdown, i.e., Input(component_id='site-dropdown', component_property='value')
# Output to be the graph with id success-pie-chart, i.e., Output(component_id='success-pie-chart', component_property='figure')
# A If-Else statement to check if ALL sites were selected or just a specific launch site was selected
# If ALL sites are selected, we will use all rows in the dataframe spacex_df to render and return 
# a pie chart graph to show the total success launches (i.e., the total count of class column)
# If a specific launch site is selected, you need to filter the dataframe spacex_df first in order to include the only data for the selected site.
# Then, render and return a pie chart graph to show the success (class=1) count and failed (class=0) count for the selected site.
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
        names='pie chart names', 
        title='title')
        return fig
    else:
        # return the outcomes piechart for a selected site


# ## Task 3: Add a Range Slider to Select Payload

# In[ ]:


# Next, we want to find if variable payload is correlated to mission outcome. From a dashboard point of view, 
# we want to be able to easily select different payload range and see if we can identify some visual patterns.
# Find and complete a commented dcc.RangeSlider(id='payload-slider',...) input with the following attribute:
# id to be payload-slider
# min indicating the slider starting point, we set its value to be 0 (Kg)
# max indicating the slider ending point to, we set its value to be 10000 (Kg)
# step indicating the slider interval on the slider, we set its value to be 1000 (Kg)
# value indicating the current selected range, we could set it to be min_payload and max_payload
# Here is an example of RangeSlider:
dcc.RangeSlider(id='id',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[min_value, max_value])


# ## Task 4: Add a callback function to render the success-payload-scatter-chart scatter plot

# In[ ]:


# Next, we want to plot a scatter plot with the x axis to be the payload and the y axis to be the launch outcome (i.e., class column).
# As such, we can visually observe how payload may be correlated with mission outcomes for selected site(s).

# In addition, we want to color-label the Booster version on each scatter point so that we may observe mission outcomes with different boosters.
# Now, let’s add a call function including the following application logic:

# Input to be [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
# Note that we have two input components, one to receive selected launch site and another to receive selected payload range
# Output to be Output(component_id='success-payload-scatter-chart', component_property='figure')
# A If-Else statement to check if ALL sites were selected or just a specific launch site was selected
# If ALL sites are selected, render a scatter plot to display all values for variable Payload Mass (kg) and variable class.
# In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
# If a specific launch site is selected, you need to filter the spacex_df first, and render a scatter chart to show values Payload Mass (kg) 
# and class for the selected site, and color-label the point using Boosster Version Category likewise.


# ## Below is the full code of the spacex_dash.py file:

# In[ ]:


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
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                         {'label': 'ALL SITES', 'value': 'ALL'},
                                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                    ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here", 
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[min_payload,max_payload],
                                                marks={0: '0', 2500:'2500',5000:'5000',
                                                7500:'7500', 10000: '10000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def build_graph(site_dropdown):
    if site_dropdown == 'ALL':
        piechart = px.pie(data_frame = spacex_df, names='Launch Site', values='class' ,title='Total Launches for All Sites')
        return piechart
    else:
        #specific_df = spacex_df['Launch Site']
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        piechart = px.pie(data_frame = specific_df, names='class',title='Total Launch for a Specific Site')
        return piechart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')])

def update_graph(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        scatterplot = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
        return scatterplot
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        filtered_data = specific_df[(specific_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        scatterplot = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
        return scatterplot

# Run the app
if __name__ == '__main__':
    app.run_server()

