import sqlite3 as sql
import csv
import random
from collections import OrderedDict
import re
from pathlib import Path

MAPS = ["Erangel", "Miramar", "Savage"]
GAME_TYPE = ["Solo", "Duo", "Squad"]
PLAYERCSV = 'player.csv'
TEAMCSV = 'teams.csv'

def drop_table(table_name, curr, conn):
    drop = """
    DROP TABLE IF EXISTS {}
    """.format(table_name)
    curr.execute(drop)
    conn.commit()
    
def create_tables(game_map: str, game_type: str, conn, curr):
    event_name = f'{game_map}{game_type}'
    drop_table(event_name, curr, conn)
    #create duo team makeup
        # team number, player, primary key (Team#Player)
    team_makeup_table_name = f'{event_name}TeamMakeup'
    create_team_makeup = """
    CREATE TABLE {}(
        team_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        PRIMARY KEY (team_id, username)
    )
    """.format(team_makeup_table_name)
    curr.execute(create_team_makeup)

    #insert DB information here
    generateGameTables(game_map, game_type, conn, curr)

    conn.commit()

    for i in range(1,4):
        team_round_stats_name = f'{event_name}TeamStatsRound{i}'
        player_round_stats_name = f'{event_name}PlayerStatsRound{i}'
        drop_table(team_round_stats_name, curr, conn)
        drop_table(player_round_stats_name, curr, conn)
        
        # duo team stats for each round
        create_team_stats_round = """
        CREATE TABLE {}(
            team_id INTEGER PRIMARY KEY NOT NULL,
            kills INTEGER NOT NULL,
            damage INTEGER NOT NULL,
            distance INTEGER NOT NULL,
            win INTEGER NOT NULL,
            headshots INTEGER NOT NULL,
            time INTEGER NOT NULL
        )
        """.format(team_round_stats_name)

        curr.execute(create_team_stats_round)

        #insert DB information here

        conn.commit()
    
        create_player_stats_round = """
        CREATE TABLE {}(
            username TEXT PRIMARY KEY NOT NULL,
            kills INTEGER NOT NULL,
            damage INTEGER NOT NULL,
            distance INTEGER NOT NULL,
            headshots INTEGER NOT NULL,
            time INTEGER NOT NULL
        )
        """.format(player_round_stats_name)

        curr.execute(create_player_stats_round)

        #insert DB information here

        conn.commit()
        
    #create total team stats
    team_total_stats_name = f'{event_name}TotalTeamStats'
    drop_table(team_total_stats_name, curr, conn)

    create_total_team_stats = """
    CREATE TABLE {}(
        team_id INTEGER PRIMARY KEY NOT NULL,
        kd REAL NOT NULL,
        damage INTEGER NOT NULL,
        win_percentage REAL NOT NULL,
        headshot_percentage REAL NOT NULL,
        average_time INTEGER NOT NULL,
        most_kills INTEGER NOT NULL,
        total_distance INTEGER NOT NULL
    )
    """.format(team_total_stats_name)

    curr.execute(create_total_team_stats)

    #insert DB information here

    conn.commit()

    award_name = f'{event_name}Awards'
    drop_table(award_name, curr, conn)
    create_awards = """
    CREATE TABLE {}(
        place INTEGER PRIMARY KEY NOT NULL,
        description TEXT NOT NULL,
        team_id INTEGER NOT NULL
    )
    """.format(award_name)
    curr.execute(create_awards)

    #insert DB information here

    conn.commit()

def create_players(conn, curr):
    drop_table('Player', curr, conn)
    create_player_table = """
    CREATE TABLE Player(
        username TEXT PRIMARY KEY NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        gender TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    """
    curr.execute(create_player_table)

    #insert DB information here
    generatePlayerTable(conn, curr)

    conn.commit()

def connect(db_name):
    data_dir = Path.cwd() / Path('Files') / '{}'.format(db_name)
    conn = sql.connect(str(data_dir))
    curr = conn.cursor()
    return conn, curr

def create_game():
    maps = ['Erangel', 'Miramar', 'Savage']
    game_types = ['Solo', 'Duo', 'Squad']
    conn, curr = connect('pubg_game_db.sqlite3')
    for game_map in maps:
        for game_type in game_types:
            create_tables(game_map, game_type, conn, curr)
            
    create_players(conn, curr)

create_game()



#######################################################
#   Functions that insert DB information into the table
#######################################################

def generatePlayerTable(conn, curr):
    """
    Fills the 'PLayer' Table with random information
    Must use create_players(conn, curr) before this function
    """
    cmd = """
    INSERT INTO Player(username, first_name, last_name, phone, address, gender, age)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """

    with open(PLAYERCSV, 'r') as f:
        #Reads from the CSV file the random generation of players
        reader = csv.DictReader(f)
        data = list(reader)
        for my_dict in data:
            l = list()  #   An appendable list to execute a tuple later
            for fields in self.FIELD_NAMES:
                l.append(my_dict[fields])
            curr.execute(cmd, tuple(l))

def generateMapGameTypeTable(game_map: str, game_type: str, noTeams: int, conn, curr):
    """
    Fills the '{game_map}{game_type}TeamMakeup' Table with random information
    Must use create_tables(game_map: str, game_type: str, conn, curr) before this function
    and must have generated all the players in the Player TABLE.

        ie:
        TABLE ErangleSquadTeamMakeup
            Team                Players
            WalmartGreeters     JimmyJur
                                JacobIr
                                SonnySir
                                CarlosJ
            ...
            ...
            SunnySideKillers    BrianBrian
                                MikeHunt
                                MauricioChills
                                SomeoneElse

    """
    noPerTeam = 0
    if game_type == 'Solo':
        noPerTeam = 1
    elif game_type == 'Duo':
        noPerTeam = 2
    elif game_type == 'Squad':
        noPerTeam = 4

    with open(TEAMCSV, 'r') as f:
        #Reads from the CSV file the random generation of teams
        reader = csv.DictReader(f)
        data = list(reader)

        i = 0   # counter to limit the number of total Teams
        teams_list = list() # helps later by checking if the team name already exists
        usernames = list() # helps later by checking if the player's username is already taken

        cmd = "SELECT username FROM Player"
        curr.execute(cmd)
        records = curr.fetchall()

        event_name = f'{game_map}{game_type}'
        team_makeup_table_name = f'{event_name}TeamMakeup'

        cmd = """
        INSERT INTO {}(team_id, username, (team_id, username))
        VALUES (?, ?, ?);
        """.format(team_makeup_table_name)
    
        while i < noTeams:
            team_players = list()                   # list of players of size noPerTeam to execute later
            team_name = random.choice(data)['team_names']
            if not team_name in teams_list:         # checks if the team name is already taken
                usernames.append(team_name)         # updates a list of taken names
                teams_list.append(team_name)        # updates the list of a team's players
                i += 1
                j = 0                               # counter to limit the number of players per team
                while j < noPerTeam:
                    player = random.choice(records)
                    if not player in team:          # checks if the player's username is taken
                        team_players.append(player) # updates a list of taken names


                curr.execute(cmd, (team_name, tuple(team_players)))
