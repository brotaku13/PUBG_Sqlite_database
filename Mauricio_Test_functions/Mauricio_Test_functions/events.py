import sqlite3 as sq
import csv


EVENTSSQL = "Events.sqlite"

class Events:

    def __init__(self):
        self.__conn = sq.connect(EVENTSSQL)
        self.__cur = self.__conn.cursor()
        self.__fieldNames = ["event_id", "event_name"]

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
        self.__dropTable("Events")

        cmd = """
        CREATE TABLE Events(
        event_id INTEGER PRIMARY KEY NOT NULL,
        event_name TEXT
        );
        """
        self.__cur.execute(cmd)

        self.__add_events()

    def __add_events(self):
        """
        Fills the 'PLayer' Table with random information
        Must use create_eventss(conn, curr) before this function
        """
        cmd = """
        INSERT INTO Events(event_id, event_name)
        VALUES (?, ?);
        """

        ###################################
        ####   Enter Algorithm Here    ####
        ###################################
        self.__cur.execute(cmd, (1, "Erangel"))
        self.__cur.execute(cmd, (2, "Miramar"))
        self.__cur.execute(cmd, (3, "Savage"))

    def see_all(self):
        cmd = "SELECT * FROM Events"
        self.__cur.execute(cmd)

        records = self.__cur.fetchall()
        self.__pretty_print(records, self.__fieldNames)

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