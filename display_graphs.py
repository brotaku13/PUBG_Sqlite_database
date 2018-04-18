import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import utility_functions

def get_players(conn, curr):
    cmd = """
    SELECT username, user_id FROM Players
    ORDER BY user_id
    LIMIT 300
    """
    curr.execute(cmd)
    players = curr.fetchall()
    # build [{username: player_id}]
    player_list = []
    for item in players:
        player_list.append({item[0]: item[1]})

    return player_list

def get_teams(conn, curr):
    cmd = """
    SELECT distinct team_id FROM Teams
    """
    curr.execute(cmd)
    teams = curr.fetchall()
    team_list = []
    for item in teams:
        team_list.append({'Team {}'.format(item[0]): item[0]})
    return team_list
    
    
def setup_layout(conn, curr, app):
    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='player_id_dropdown',
                    options=get_players(conn, curr),
                    value='Player ID'
                )
            ],
            style={'width': '49%', 'display': 'inline-block'}),  # style of player_id Dropdown

            html.Div([
                dcc.Graph(
                    id='player_bar'
                )
            ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),  # style of player_bar

            html.Div([
                dcc.Dropdown(
                    id='team_id_dropdown',
                    options=get_teams(conn, curr),
                    value='Team ID'
                )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),  # style of team_id_dropdown

             html.Div([
                dcc.Graph(
                    id='team_bar'
                    )
            ], style={'display': 'inline-block', 'width': '49%'}),  # style of team_bar

        # total layout style
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

    ])


def run_dash(conn, curr):
    app = dash.Dash()
    setup_layout(conn, curr, app)
    app.run_server()
    return False
