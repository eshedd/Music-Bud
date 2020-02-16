import requests
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

user = 'Shreath'
key = '92e8557a82a1a5dae48a89f63037f9be'  # public api key
limit = 1000
pages = ['1','2', '3', '4', '5', '6']

total = 1
artist_mbids = []
artist_names = []
song_mbids = []
song_names = []

payload = {}
headers = {}

df = pd.DataFrame()

artist_dicts = []
for page in pages:
    json_data = requests.request('GET', 'http://ws.audioscrobbler.com/2.0/?method={}&user={}&limit={}&api_key={}&page={}&format=json'.format(
        'user.getrecenttracks', user, limit, key, page), headers=headers, data=payload)
    list_data = json_data.json()["recenttracks"]["track"]
    print('length', len(list_data))
    for i in range(len(list_data)):
        artist = list_data[i]["artist"]["#text"]
        song = list_data[i]["name"]
        date = list_data[i]["date"]["#text"]
        tag_json_data = requests.request('GET', 'http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&artist={}&api_key={}&format=json'.format(
            artist, key), headers=headers, data=payload)
        # print(tag_json_data.json())
        # if "error" not in tag_json_data.json():
        print(tag_json_data.json())
        # tag_list_data = tag_json_data.json()["toptags"]["tag"]
        # top_tags = []
        # if len(tag_list_data) != 0:  # check that there are tags to print
        #     for tag in tag_list_data[:min(len(tag_list_data), 5)]:
        #         top_tags.append(tag["name"])
        #     dict_row = {'Index': total, 'Artist': artist, 'Song': song, 'Date': date, 'Top Tag': top_tags}
        # else:
        #     dict_row = {'Index': total, 'Artist': artist, 'Song': song, 'Date': date}
        total += 1
    print(dict_row)



#print(df.head())

#df = pd.DataFrame(data["recenttracks"]["track"])

for index, row in df.iterrows():
    song_names.append(row['name'])
    artist_names.append(row['artist']['#text'])

#artist_df = df['artist']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(children=[
        html.H1(
            children='Hello Dash',
            style={
                'textAlign': 'center'
            }
        ),
        dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'Artists', 'value': 'artist'},
                {'label': 'Songs', 'value': 'song'},
            ],
            value = 'artist'
        ),
        dcc.Graph(id='my-chart')
    ]
)

# @app.callback(
#     Output(component_id='my-chart', component_property='figure'),
#     [Input(component_id='my-dropdown', component_property='value')]
# )
# def update_output_div(info_type):
#
#     counts = artist_df.value_counts()
#
#     return {
#         'data': [{
#             'x': artist_names,
#             'y': counts,
#             'type': 'bar'
#         }],
#         'layout': {
#             'title': 'Dash Data Visualization'
#         }
#     }
if __name__ == '__main__':
    app.run_server(debug=True)
