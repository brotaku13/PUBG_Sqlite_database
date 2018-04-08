from players import Players
import random
import sqlite3 as sq
import csv


PLAYERSTATSSQL = "PlayerStats.sqlite"

class PlayerStats:
    def __init__(self, player):
        self.__conn = sq.connect(PLAYERSTATSSQL)
        self.__cur = self.__conn.cursor()
        self.__fieldNames = ["username", "event_id", "team_id", "kills", "damage", "distance", "headshots", "time", "death"]
        self.__player = player
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
        death BIT
        );
        """
        self.__cur.execute(cmd)

        self.__add_playerstats()

########################################################################
#   Here Starts functions that fill up the player stats
########################################################################
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

        playerRecords = self.__player.getRecords("SELECT * FROM Players") #playerRecords[1] is username
        event_id = random.choice(range(1,4)) #choose randomly if the game is solo, duo, or squad
        team_id = list()
        kills = self.__getKills()
        distance = list(map(lambda x: 10 * random.choice(range(1, 101)), list(range(1, 101))))
        time = list(map(lambda x: 10 * random.choice(range(1, 101)), list(range(1, 101))))
        death = list(map(lambda x: 0, list(range(1, 101))))

        found = False
        while not found:
            choose = random.choice(range(1,100))
            if kills[choose] > 0:
                death[choose] = 1
                found = True

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

        for i in range(0, 100):
            self.__cur.execute(cmd, (playerRecords[i][1], event_id, team_id[i], kills[i], kills[i] * 100, distance[i], random.choice(range(0, kills[i] + 1)), time[i], death[i]))

    def __getKills(self):
        kills = 99
        killList = list()
        for i in range(0, 100):
            choice = random.choice(range(0, 5))
            if choice > kills:
                killList.append(kills)
            elif choice <= kills:
                kills -= choice
                killList.append(choice)
        return killList

########################################################################
#   Here Ends functions that fill up the player stats
########################################################################

    def see_all(self):
        cmd = "SELECT * FROM PlayerStats"
        self.__cur.execute(cmd)

        records = self.__cur.fetchall()
        self.__pretty_print(records, self.__fieldNames)

    def getRecords(self, cmd):
        self.__cur.execute(cmd)
        return self.__cur.fetchall()

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