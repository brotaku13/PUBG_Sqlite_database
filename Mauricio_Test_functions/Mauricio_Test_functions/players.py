import sqlite3 as sq
import csv



PLAYERCSV = "players.csv"
PLAYERSQL = "Players.sqlite"

class Players:

    def __init__(self):
        self.__conn = sq.connect(PLAYERSQL)
        self.__cur = self.__conn.cursor()
        self.__fieldNames = ["id", "username", "first_name", "last_name", "phone", "address", "gender", "age"]

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
        self.__dropTable("Players")

        cmd = """
        CREATE TABLE Players(
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        phone INTEGER,
        address TEXT,
        gender TEXT,
        age INTEGER
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
        INSERT INTO Players(id, username, first_name, last_name, phone, address, gender, age)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """

        with open(PLAYERCSV, 'r') as f:
            #Reads from the CSV file the random generation of players
            reader = csv.DictReader(f)
            data = list(reader)
            for my_dict in data:
                l = list()  #   An appendable list to execute a tuple later
                for fields in self.__fieldNames:
                    l.append(my_dict[fields])
                self.__cur.execute(cmd, tuple(l))

    def see_all(self):
        cmd = "SELECT * FROM Players"
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