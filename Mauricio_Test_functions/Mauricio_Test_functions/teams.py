import sqlite3 as sq
import csv



TEAMSCSV = "teams.csv"
TEAMSSQL = "Teams.sqlite"

class Teams:

    def __init__(self, player, event):
        self.__conn = sq.connect(TEAMSSQL)
        self.__cur = self.__conn.cursor()
        self.__fieldNames = ["team_id", "username", "event_id"]
        self.__player = player
        self.__event = event
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
        self.__dropTable("Teams")

        cmd = """
        CREATE TABLE Teams(
        team_id INTEGER,
        username TEXT PRIMARY KEY NOT NULL,
        event_id INTEGER
        );
        """
        self.__cur.execute(cmd)

        self.__add_player()

    def __add_player(self):
        """
        Fills the 'PLayer' Table with random information
        Must use create_players(conn, curr) before this function
        """
        cmd = """
        INSERT INTO Teams(team_id, username, event_id)
        VALUES (?, ?, ?);
        """

        ###################################
        ####   Enter Algorithm Here    ####
        ###################################
        
        team_id = list()

        eventRecords = self.__event.getRecords("SELECT * FROM Events")
        event_id = eventRecords[0][0]

        if event_id == 1:
            #solo
            team_id = list(range(1, 101))
        elif event_id == 2:
            #duo
            for i in range(1, 51):
                team_id.append(i)
                team_id.append(i)
        elif event_id == 3:
            #squad
            for i in range(1, 26):
                team_id.append(i)
                team_id.append(i)
                team_id.append(i)
                team_id.append(i)

        playerRecords = self.__player.getRecords("SELECT * FROM Players")

        for i in range(0, 100):
            self.__cur.execute(cmd, (team_id[i], playerRecords[i][1], event_id))

    def see_all(self):
        cmd = "SELECT * FROM Teams"
        self.__cur.execute(cmd)

        records = self.__cur.fetchall()
        self.__pretty_print(records, self.__fieldNames)

    def getRecords(self, cmd):
        self.__cur.execute(cmd)
        return self.__cur.fetchall()

    def __pretty_print(self, records, column_headers):
        """Pretty print the records with given column headers"""
        # Create a format string making each column left aligned and 30 characters wide
        fmt_string = "{:<30}" * len(column_headers)

        # Print header row
        print(fmt_string.format(*column_headers))

        # Print records
        # records is a list of tuples
        # each tuple is a specific record in the database
        # *row expands the tuple into separate arguments for format
        for row in records:
            print(fmt_string.format(*row))