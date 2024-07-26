from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# List of file names
file_names = ['temp_data_air.csv', 'temp_data_surface.csv', 'temp_data_1m.csv', 'temp_data_2m.csv', 'temp_data_3m.csv', 'temp_data_4m.csv', 'temp_data_5m.csv']
depth = -1
df = pd.DataFrame()

# Read and process each file
for file in file_names:
    with open(file, 'r') as file_obj:
        data = file_obj.read()
    
    # Check if the header is correct
    if not data.startswith('Datetime,header,id,temperature\n'):
        with open(file, 'w') as file_obj:
            file_obj.write('Datetime,header,id,temperature\n')
            file_obj.write(data)
    
    temp = pd.read_csv(file)
    temp['depth'] = depth
    temp['time'] = temp.index
    depth += 1
    df = pd.concat([df, temp], ignore_index=True)

# Create the box plot figure
fig = px.box(df, x='depth', y='temperature')

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(
        figure=fig,
        style={'height': '80vh', 'width': '60vw'}  # Adjust these values as needed
    )
], style={'height': '100%', 'margin': 'auto', 'width': '100%'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


