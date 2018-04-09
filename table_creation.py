import sqlite3 as sql
import csv
from pathlib import Path

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
    """
    Creates the awards table
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

    drop_table('Awards', conn, curr)
    cmd = """
    CREATE TABLE Awards(
    event_id INTEGER KEY NOT NULL,
    place INTEGER,
    team_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (event_id, place),
    FOREIGN KEY(event_id) REFERENCES Events(event_id),
    FOREIGN KEY(team_id) REFERENCES Teams(team_id),
    FOREIGN KEY(user_id) REFERENCES Players(user_id)
    )
    """
    curr.execute(cmd)
    conn.commit()

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
    num_teams INTEGER NOT NULL
    )
    """
    curr.execute(cmd)
    conn.commit()


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
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY(user_id) REFERENCES Players(user_id),
    FOREIGN KEY(event_id) REFERENCES Events(event_id),
    FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    )
    """
    curr.execute(cmd)
    conn.commit()

def add_players(conn, curr):
    """
    adds players from the players.csv into the Players table
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """

    cmd = """
    INSERT INTO Players(user_id, username, first_name, last_name, phone, address, gender, age)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    PLAYERCSV = "players.csv"
    fieldNames = ["user_id", "username", "first_name", "last_name", "phone", "address", "gender", "age"]

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

def add_events(events, conn, curr):
    """
    adds events to the Events table and automatically assigns the event ID
    :param: events [list] -- a list of tuples in (event_name, num_teams) format
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    for event in events:
        add_event = """
        INSERT INTO Events(event_name, num_teams)
        VALUES(?, ?)
        """
        curr.execute(add_event, event)
        conn.commit()

def create_tables(events, curr, conn):
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
    add_players(conn, curr)
    add_events(events, conn, curr)

