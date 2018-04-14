import utility_functions
from collections import OrderedDict
import table_creation
import plotly
from plotly.graph_objs import Bar, Layout
from pathlib import Path

TEAM_1 = [(1,1,1, 0, 32, 1111, 0, 382, 1, 1111), (1,1,1, 0, 32, 222, 0, 382, 1, 222), (1,1,1, 0, 32, 333, 0, 382, 1, 333), (1,1,1, 0, 32, 121, 0, 382, 1, 150)]

CURR = utility_functions.CURR
PATH = Path(Path.cwd()) / Path("Files")

def playerstats(user_id):
    """
    Use this function by adding the user_id as the argument. It can be done in
    a number of ways:

    playerstats(3)      #can take one user id
    playerstats([2,3])  #or can run multiple user ids

    """
    fieldnames = ['user_id', 'event_id', 'team_id', 'kills', 'damage', 'distance', 'headshots', 'time', 'death', 'score']
    title = "Player Stats for User_ID: {}"
    cmd = """
    SELECT * FROM PlayerStats
    WHERE PlayerStats.user_id = {}
    """
    if isinstance(user_id, list):
        if len(user_id) > 0:
            playerstats(user_id[1:])
            playerstats(user_id[0])
    else:
        cmd = cmd.format(user_id)
        records = CURR.execute(cmd).fetchall()
        if len(records) > 1:
            values = [[x[i] for x in records] for i in range(len(records[0]))][3:]
            groups = [("Event ID: " + str(x)) for x in [x[1] for x in records]]
            dict_list = []
            for i, field in enumerate(fieldnames[3:]):
                dict_list.append(my_dict(groups, values[i], field))
            grouped(title.format(user_id), dict_list)

        else:
            basic(title.format(user_id), fieldnames[3:], list(records[0])[3:])

def teamstats(team_id):
    """
    Use this function by adding the team_id as the argument. It can be done in
    a number of ways:

    teamstats(3)      #can take one user id
    teamstats([2,3])  #or can run multiple user ids

    """
    fieldnames = ['user_id', 'event_id', 'team_id', 'kills', 'damage', 'distance', 'headshots', 'time', 'death', 'score']
    title = "Team Stats for Team_ID: {}"
    cmd = """
    SELECT * FROM PlayerStats
    WHERE PlayerStats.team_id = {}
    """
    if isinstance(team_id, list):
        if len(team_id) > 0:
            teamstats(team_id[1:])
            teamstats(team_id[0])
    else:
        cmd = cmd.format(team_id)
        records = CURR.execute(cmd).fetchall()
        stats = [[str(field[0].upper()+field[1:] + " @ Event_" + str(x[1])) for y,
                field in enumerate(fieldnames[3:])] for i, x in enumerate(records)]
        dict_list = []
        if len(records) > 1:
            for playerNum, rec in enumerate(records):
                record = list(rec)[3:]
                iD = "Team_" + str(rec[2]) + ":Player_" + str(rec[0])
                dict_list.append(my_dict(stats[playerNum], record, iD))
                print("Records" + str(records))
                print("record: " + str(record))
                print("stats: " + str(stats))
                print("stats[{}]: ".format(playerNum) + str(stats[playerNum]))
                print("iD: " + str(iD))
            stacked(title.format(team_id), dict_list)

        else:
            values = list(records[0][3:])
            iD = "Team_" + str(records[0][2]) + ":Player_1"
            print("values: " + str(values))
            print("records: " + str(records))
            print("stats: " + str(stats))
            print("iD: " + str(iD))
            dict_list.append(my_dict(stats[0], values, iD))
            stacked(title.format(team_id), dict_list)

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
    plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))

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
    layout = plotly.graph_objs.Layout(barmode='stack', title=title)
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))

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
        data.append(plotly.graph_objs.Bar(
        x=my_dict['groupName'],
        y=my_dict['values'],
        name=my_dict['barName']
        ))

    layout = plotly.graph_objs.Layout(barmode='group', title=title)
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=str(PATH)+'/{}.html'.format(title))

def my_dict(x,y,z):
    return OrderedDict([('groupName', x), ('values', y), ('barName', z)])