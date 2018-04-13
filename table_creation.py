import sqlite3 as sql
import csv
from pathlib import Path
import utility_functions

def drop_table(table_name, conn, curr):
    """
    Drops the table if it exists
    :param: table_name [str] -- name of the table to drop
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    drop = """
    DROP TABLE IF EXISTS {}
    """.format(table_name)
    curr.execute(drop)
    conn.commit()

def create_awards(conn, curr):
    
    drop_table('Awards', conn, curr)
    cmd = """
    CREATE TABLE Awards(
        award_id INTEGER PRIMARY KEY NOT NULL,
        event_id INTEGER NOT NULL,
        place TEXT NOT NULL,
        description TEXT NOT NULL,
        team_id INTEGER NOT NULL,
        FOREIGN KEY(event_id) REFERENCES Events(event_id)
        FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    )
    """
    curr.execute(cmd)
    conn.commit()
    return curr.fetchall()

def create_events(conn, curr):
    """
    Creates the events table
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

    drop_table('Events', conn, curr)
    cmd = """
    CREATE TABLE Events(
    event_id INTEGER PRIMARY KEY NOT NULL,
    event_name TEXT NOT NULL,
    round INTEGER NOT  NULL,
    game_number INTEGER NOT NULL,
    num_teams INTEGER NOT NULL
    )
    """
    curr.execute(cmd)
    conn.commit()
    return curr.fetchall()

def create_teams(conn, curr):
    """
    Creates the Teams table
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

    drop_table('Teams', conn, curr)
    cmd = """
    CREATE TABLE Teams(
    user_id INTEGER,
    event_id TEXT NOT NULL,
    team_id INTEGER,
    PRIMARY KEY(user_id, event_id),
    FOREIGN KEY(event_id) REFERENCES Events(event_id),
    FOREIGN KEY(user_id) REFERENCES Players(user_id)
    )
    """
    curr.execute(cmd)
    conn.commit()
    return curr.fetchall()

def create_players(conn, curr):
    """
    Creates the Players table
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

    drop_table('Players', conn, curr)
    cmd = """
    CREATE TABLE Players(
    user_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone INTEGER NOT NULL,
    address TEXT NOT NULL,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL
    )
    """
    curr.execute(cmd)
    conn.commit()
    return curr.fetchall()

def create_playerstats(conn, curr):
    """
    Creates the PlayerStats table
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

    drop_table('PlayerStats', conn, curr)
    cmd = """
    CREATE TABLE PlayerStats(
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    team_id INTEGER,
    kills INTEGER,
    damage INTEGER,
    distance INTEGER,
    headshots INTEGER,
    time INTEGER,
    death BIT,
    score INTEGER,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY(user_id) REFERENCES Players(user_id),
    FOREIGN KEY(event_id) REFERENCES Events(event_id),
    FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    )
    """
    curr.execute(cmd)
    conn.commit()
    return curr.fetchall()

def create_team_scores(conn, curr):
    drop_table('TeamScores', conn, curr)
    cmd = """
    CREATE TABLE TeamScores(
        team_id INTEGER,
        event_id INTEGER, 
        score INTEGER,
        PRIMARY KEY(team_id, event_id),
        FOREIGN KEY(event_id) REFERENCES Events(event_id),
        FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    )
    """
    curr.execute(cmd)
    conn.commit()
    return curr.fetchall()

def add_players(conn, curr):
    """
    adds players from the players.csv into the Players table
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

    cmd = """
    INSERT INTO Players(username, first_name, last_name, phone, address, gender, age)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    PLAYERCSV = "player_data.csv"
    fieldNames = ["username", "first_name", "last_name", "phone", "address", "gender", "age"]

    with open(PLAYERCSV, 'r') as f:
        #Reads from the CSV file the random generation of players
        reader = csv.DictReader(f)
        data = list(reader)
        for my_dict in data:
            l = list()  #   An appendable list to execute a tuple later
            for fields in fieldNames:
                l.append(my_dict[fields])
            curr.execute(cmd, tuple(l))
            conn.commit()
    return curr.fetchall()

def add_events(events, conn, curr):
    """
    adds events to the Events table and automatically assigns the event ID
    :param: events [list] -- a list of tuples in (event_name, num_teams) format
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    for event in events:
        event_name = event[0]
        num_teams = event[1]
        for game_round in range(1, 4):  # 3 rounds 1 game less each round
            for game_num in range(0, 3 - (game_round - 1)):
                add_event = """
                INSERT INTO Events(event_name, round, game_number, num_teams)
                VALUES(?, ?, ?, ?)
                """
                curr.execute(add_event, (event_name, game_round, game_num + 1, num_teams))
                conn.commit()
    return curr.fetchall()

def add_awards(events, awards, conn, curr):
    for i in range(len(events)):
        event_name = events[i][0]
        event_awards = awards[i]
        for place, description in event_awards.items():
            insert = """
            INSERT INTO Awards(event_id, place, description, team_id)
            VALUES(?, ?, ?, ?)
            """
            curr.execute(insert, (6, place, description, 0))
            conn.commit()
    return curr.fetchall()

def create_tables(events, awards, conn, curr):
    """
    Creates all necessary tables for the database
    :param: events [list] -- a list of tuples in (event_name, num_teams) format
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    create_players(conn, curr)
    create_events(conn, curr)
    create_teams(conn, curr)
    create_awards(conn, curr)
    create_playerstats(conn, curr)
    create_team_scores(conn, curr)
    add_players(conn, curr)
    add_events(events, conn, curr)
    add_awards(events, awards, conn, curr)
    utility_functions.print_all(curr)

def is_redundant(curr):
    try:
        rowsCSV = 0
        with open(PLAYER_DATA, 'r') as f:
            #Reads from the CSV file the random generation of players
            reader = csv.DictReader(f)
            data = list(reader)
            rowsCSV = len(data)
        records = utility_functions.list_players()
        rowsSQL = len(records)

        return rowsSQL == rowsCSV
    except Exception:
        return False

def is_event_redundant(curr, events):
    try:
        if len(utility_functions.display_player_by_name()) == 0:
            return False
        if len(utility_functions.list_players()) == 0:
            return False
        if len(utility_functions.male_players()) == 0:
            return False
        if len(utility_functions.female_players()) == 0:
            return False
        if len(utility_functions.list_events()) == 0:
            return False
    except Exception:
        return False
    return True