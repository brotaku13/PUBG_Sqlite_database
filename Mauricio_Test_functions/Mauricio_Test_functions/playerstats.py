import sqlite3 as sq
import csv


PLAYERSTATSSQL = "PlayerStats.sqlite"

class PlayerStats:
    def __init__(self):
        self.__conn = sq.connect(PLAYERSTATSSQL)
        self.__cur = self.__conn.cursor()
        self.__fieldNames = ["username", "event_id", "team_id", "kills", "damage", "distance", "headshots", "time", "death"]

        self.__create_table()

    def __dropTable(self, tables):
        cmd = "DROP TABLE IF EXISTS {}"
        
        if isinstance(tables, list):
            for table in tables:
                drop = cmd.format(table)
                self.__cur.execute(drop)
        elif isinstance(tables, str):
            drop = cmd.format(tables)
            self.__cur.execute(drop)

    def __create_table(self):
        self.__dropTable("PlayerStats")

        cmd = """
        CREATE TABLE PlayerStats(
        username TEXT PRIMARY KEY NOT NULL,
        event_id INTEGER NOT NULL,
        team_id INTEGER,
        kills INTEGER,
        damage INTEGER,
        distance INTEGER,
        headshots INTEGER,
        time INTEGER,
        death INTEGER
        );
        """
        self.__cur.execute(cmd)

        self.__add_playerstats()

    def __add_playerstats(self):
        """
        Fills the 'PLayer' Table with random information
        Must use create_players(conn, curr) before this function
        """
        cmd = """
        INSERT INTO PlayerStats(username, event_id, team_id, kills, damage, distance, headshots, time, death)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        total_kills_possible = 99

        ###################################
        ####   Enter Algorithm Here    ####
        ###################################
        self.__cur.execute(cmd, ("someUsername3", 3, 3, 4, 100, 1000, 2, 3459, 1))
        self.__cur.execute(cmd, ("someUsername1", 3, 2, 4, 100, 1000, 2, 3459, 0))
        self.__cur.execute(cmd, ("someUsername2", 3, 1, 4, 100, 1000, 2, 3459, 0))


    def see_all(self):
        cmd = "SELECT * FROM PlayerStats"
        self.__cur.execute(cmd)

        records = self.__cur.fetchall()
        self.__pretty_print(records, self.__fieldNames)

    def __pretty_print(self, records, column_headers):
        """Pretty print the records with given column headers"""
        # Create a format string making each column left aligned and 30 characters wide
        fmt_string = "{:<15}" * len(column_headers)

        # Print header row
        print(fmt_string.format(*column_headers))

        # Print records
        # records is a list of tuples
        # each tuple is a specific record in the database
        # *row expands the tuple into separate arguments for format
        for row in records:
            print(fmt_string.format(*row))