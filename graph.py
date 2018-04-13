import utility_functions
import table_creation
import plotly
from plotly.graph_objs import Bar, Layout
from pathlib import Path

def create(records):
    #########grouped chart###############

    trace1 = plotly.graph_objs.Bar(
        x=['Team1', 'Team2', 'Team3'],
        y=[2, 4, 3],
        name='Kills'
    )
    trace2 = plotly.graph_objs.Bar(
        x=['Team1', 'Team2', 'Team3'],
        y=[1, 2, 4],
        name='Kills'
    )
    data = [trace1, trace2]
    layout = plotly.graph_objs.Layout(barmode='group'
    )
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='grouped-bar.html')



    ###   Stacked Chart   ####
    trace1 = plotly.graph_objs.Bar(
        x=['Team1', 'Team2', 'Team3'],
        y=[2, 4, 3],
        name='Kills'
    )
    trace2 = plotly.graph_objs.Bar(
        x=['Team1', 'Team2', 'Team3'],
        y=[3, 1, 4],
        name='Kills'
    )
    data = [trace1, trace2]
    layout = plotly.graph_objs.Layout(
        barmode='stack'
    )
    fig = plotly.graph_objs.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='stacked-bar.html')