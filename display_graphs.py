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
            dcc.Dropdown(
                id='team_id_dropdown',
                options=team_list,
                value=1
            )],style={}),
        html.Div([
            html.Div([  # total area (left side)
                html.Div([  # left
                    dcc.Graph(id='player_a'),
                    dcc.Graph(id='player_b')
                ], style={'display': 'table-cell', 'padding': '0px 0px 0px 0px', 'width':'30vw'}),

                html.Div([  # right
                    dcc.Graph(id='player_c'),
                    dcc.Graph(id='player_d')
                ], style={'display': 'table-cell', 'padding': '0px 0px 0px 0px', 'width':'30vw'})

            ],style={'width': '60%', 'display': 'table-cell', 'padding': '0px 0px 0px 0px', 'width':'60vw'}),

            html.Div([  # right side
                dcc.Graph(
                    id='team_bar',
                    style={'height': '90vh'}
                    )
            ], style={'width': '38vw', 'display': 'table-cell', 'padding': '0px 0px 0px 0px'}),

        # total layout style
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '5px 5px',
            'height': '100vh',
            'display': 'table-row'
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

    player_graphs = ['player_a', 'player_b', 'player_c', 'player_d']

    @app.callback(
    Output(component_id='team_bar', component_property='figure'),
    [Input(component_id='team_id_dropdown', component_property='value')]
    )
    def update_player_output_div(input_value):
        return graph.teamstats(input_value, conn, curr)

    @app.callback(
        Output(component_id='player_a', component_property='figure'),
        [Input(component_id='team_id_dropdown', component_property='value')]
    )
    def update_player_graph_a(input_value):
        player_position = 0
        return graph.playerstats(input_value, conn, curr, player_position)

    @app.callback(
        Output(component_id='player_c', component_property='figure'),
        [Input(component_id='team_id_dropdown', component_property='value')]
    )
    def update_player_graph_a(input_value):
        player_position = 1
        return graph.playerstats(input_value, conn, curr, player_position)

    @app.callback(
        Output(component_id='player_b', component_property='figure'),
        [Input(component_id='team_id_dropdown', component_property='value')]
    )
    def update_player_graph_a(input_value):
        player_position = 2
        return graph.playerstats(input_value, conn, curr, player_position)

    @app.callback(
        Output(component_id='player_d', component_property='figure'),
        [Input(component_id='team_id_dropdown', component_property='value')]
    )
    def update_player_graph_a(input_value):
        player_position = 3
        return graph.playerstats(input_value, conn, curr, player_position)


    app.run_server(port=8066)

run_dash()