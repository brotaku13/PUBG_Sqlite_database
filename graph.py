import utility_functions
from collections import OrderedDict
import table_creation
import plotly
from plotly.graph_objs import Bar, Layout
from pathlib import Path

def playerstats(team_id, conn, curr, player_position):
    find_players = """
    SELECT user_id FROM Teams
    WHERE team_id=?
    """
    curr.execute(find_players, (team_id,))
    teammates = curr.fetchall()

    user_id = teammates[player_position][0]

    cmd = """
    SELECT event_id, kills, headshots, damage, distance FROM Playerstats
    WHERE user_id=?
    """
    curr.execute(cmd, (user_id,))
    stats = curr.fetchall()

    player_dict = {}
    data = []
    partitions = ['Kills', 'Headshots', 'Damage', 'Distance']
    title = 'Point Breakdown for Player {}'.format(user_id)
    for event in stats:
        event_id = event[0]
        kills = event[1]
        headshots = event[2]
        damage = event[3]
        distance = event[4]
        player_dict[event_id] = [kills * 1000, headshots * 1000, damage, distance]
    
    for event, stats in player_dict.items():
        data.append(
            Bar(
                x=partitions,
                y=stats,
                name='Event {}'.format(event)
            )
        )

    layout = Layout(
        barmode='group',
        title=title,
        yaxis=dict(
            title='Points'
        ),
        xaxis=dict(
            title='Point Breakdown'
        )
    )
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    return fig


def teamstats(team_id, conn, curr):
    """
    Use this function by adding the team_id as the argument. It can be done in
    a number of ways:

    teamstats(3)      #can take one user id
    teamstats([2,3])  #or can run multiple user ids

    """
    
    title = "Team Points Breakdown for Team {}".format(team_id)
    cmd = """
    SELECT user_id, event_id, team_id, score FROM PlayerStats
    WHERE team_id={}
    """.format(team_id)
    curr.execute(cmd)
    teamscores = curr.fetchall()
    player_dict = {}
    event_set = set()
    data = []
    for player in teamscores:
        user_id = player[0]
        event_id = player[1]
        score = player[3]
        if user_id in player_dict:
            player_dict[user_id][event_id] = score
        else:
            player_dict[user_id] = {event_id: score}
        event_set.add(event_id)

    for player, score in player_dict.items():
        scores = []
        for event_id in event_set:
            scores.append(player_dict[player][event_id])
        width = 0
        if len(event_set) == 1:
            data.append(
                Bar(
                    x=['event {}'.format(str(event_id)) for event_id in list(event_set)],
                    y=scores,
                    name='Player ID {}'.format(player),
                    width=.4
                )
            )
        else:
            data.append(
                Bar(
                    x=['event {}'.format(str(event_id)) for event_id in list(event_set)],
                    y=scores,
                    name='Player ID {}'.format(player),
                )
            )
    layout = Layout(
        barmode='stack',
        title=title,
        yaxis=dict(
            title='Points'
        ),
        xaxis=dict(
            title='Events'
        )
    )
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    return fig


def basic(title, fieldnames, values):
    """
    Example:
    basic("The Title", ["Bar_1", "Bar_2"],[1,2])
    """
    data = [plotly.graph_objs.Bar(
            x=fieldnames,
            y=values
    )]
    layout = plotly.graph_objs.Layout(title=title)
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    #plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))
    return fig

def stacked(title, dictList):
    """
    Example:
    a = [
    graph.my_dict(['Team1','Team2','team3'], [1,2,3], 'kills'),
    graph.my_dict(['Team1','Team2','team3'], [1,1,1], 'deaths'),
    graph.my_dict(['Team1','Team2','team3'], [7,8,9], 'distance')]

    grouped(a)
    """
    data = list()
    for my_dict in dictList:
        data.append(plotly.graph_objs.Bar(
            x=my_dict['groupName'],
            y=my_dict['values'],
            name=my_dict['barName']
        ))
    layout = plotly.graph_objs.Layout(
        barmode='stack', 
        title=title)
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    #plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))
    return fig

def grouped(title, dictList):
    """
    Example:
    a = [
    graph.my_dict(['Team1','Team2','team3'], [1,2,3], 'kills'),
    graph.my_dict(['Team1','Team2','team3'], [1,1,1], 'deaths'),
    graph.my_dict(['Team1','Team2','team3'], [7,8,9], 'distance')]

    grouped(a)
    """
    data = list()
    for my_dict in dictList:
        data.append(Bar(
            x=my_dict['groupName'],
            y=my_dict['values'],
            name=my_dict['barName']
        ))

    layout = plotly.graph_objs.Layout(barmode='group', title=title)
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    #plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))
    return fig

def my_dict(x,y,z):
    return OrderedDict([('groupName', x), ('values', y), ('barName', z)])