import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import utility_functions
from dash.dependencies import Input, Output
import graph

def get_players(conn, curr):
    """
    gets all of the player user_ids to sinsert into the dropdwn menus
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

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
        player_list.append({'label': '{}, ID: {}'.format(item[0], item[1]), 'value': item[1]})
    return player_list

def get_teams(conn, curr):
    """
    gets all of the team id's to insert into the drop down menus
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

    cmd = """
    SELECT distinct team_id FROM Teams
    """
    curr.execute(cmd)
    teams = curr.fetchall()
    team_list = []
    for item in teams:
        team_list.append({'label': 'Team {}'.format(item[0]), 'value': item[0]})

    return team_list
    
    
def setup_wide_layout(conn, curr, app, player_list, team_list):
    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='player_id_dropdown',
                    options=player_list,
                    value='Player ID'
                ),
                dcc.Graph(
                    id='player_bar'
                ),
                dcc.Dropdown(
                    id='team_id_dropdown',
                    options=team_list,
                    value='Team ID'
                ),
                dcc.Graph(
                    id='team_bar'
                    )
            ],
            style={'width': '100%', 'display': 'inline-block', 'align': 'center'}),  # style of player_id Dropdown

        # total layout style
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
            })
    ])

def setup_tall_layout(conn, curr, app, player_list, team_list):
    """
    Sets up the layout for the dash control panel. 
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    :param: app [Dash.app] -- an app object from the Dash library
    :param: player_list [list] -- a list containing the players to be inserted into the dropdown menu
    :param: team_list [list] -- a list containing the teams to be inserted into the dropdown menu
    """

    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='player_id_dropdown',
                    options=player_list,
                    value=1
                ),
                dcc.Graph(
                    id='player_bar',
                    style={'height': '90vh'}
                )
            ],
            style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='team_id_dropdown',
                    options=team_list,
                    value=1
                ),
                dcc.Graph(
                    id='team_bar',
                    style={'height': '90vh'}
                    )
            ],
            style={'width': '50%','float': 'right', 'display': 'inline-block'}),

        # total layout style
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px',
            'height': '100%'
            })
    ])


def run_dash():
    """
    runs the dash app
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    conn, curr = utility_functions.connect()
    app = dash.Dash()
    player_list = get_players(conn, curr)
    team_list = get_teams(conn, curr)
    setup_tall_layout(conn, curr, app, player_list, team_list)

    @app.callback(
    Output(component_id='player_bar', component_property='figure'),
    [Input(component_id='player_id_dropdown', component_property='value')]
    )
    def update_player_output_div(input_value):
        return graph.playerstats(input_value, curr)

    @app.callback(
    Output(component_id='team_bar', component_property='figure'),
    [Input(component_id='team_id_dropdown', component_property='value')]
    )
    def update_player_output_div(input_value):
        return graph.teamstats(input_value, conn, curr)


    app.run_server(port=8045)
