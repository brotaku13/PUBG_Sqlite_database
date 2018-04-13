import utility_functions
from collections import OrderedDict
import table_creation
import plotly
from plotly.graph_objs import Bar, Layout
from pathlib import Path


CURR = utility_functions.CURR
PATH = Path(Path.cwd()) / Path("Files")
def playerstats(user_id):
    """
    Use this function anywhere by adding the user_id as the argument. It can be done in
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