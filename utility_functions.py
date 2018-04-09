import sqlite3 as sql
import table_creation
from pathlib import Path

def display_player_by_name(curr):
    """
    Displays players by name
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT first_name, last_name FROM Players
    """
    print_table(cmd, 'Display user by name', curr)

def list_players(curr):
    """
    Displays all players
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    """
    print_table(cmd, 'Display all Players', curr)

def male_players(curr):
    """
    Displays all male players
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    WHERE gender='Male'
    """
    print_table(cmd, 'Display all Male Players', curr)

def female_players(curr):
    """
    Displays all female players
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    WHERE gender='Female'
    """
    print_table(cmd, 'Display all female Players', curr)

def list_events(curr):
    """
    Displays all events
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT event_name FROM Events
    """
    print_table(cmd, 'Display all Events', curr)

def players_by_event(curr):
    """
    Displays all players by event
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    pass

def winners_by_event(curr):
    """
    Displays all winners of each event (uses award table)
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    pass

def lookup_id(name: str, event: str, age: int, curr):
    """
    Looks up id by name, event, and age
    :param: name [str] -- first and last name of Player to look up
    :param: event [str] -- event the player participated in
    :param: age [int] -- age of player
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    first_name = name.split()[0]
    last_name = name.split()[1]
    cmd = """
    SELECT user_id FROM Players 
    WHERE first_name=? AND last_name=? AND age=?
    AND ? IN (
        SELECT event_name FROM Events
        )
    """
    print_table(cmd, 'Display all Events', curr, args=(first_name, last_name, age, event))

def run_all(curr, conn):
    """
    Runs all necessary functions. mostly used for utility and testing
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    display_player_by_name(curr)
    list_players(curr)
    male_players(curr)
    female_players(curr)
    list_events(curr)


def print_table(cmd, table_name, curr, args=()):
    """
    Prints a table in a readable format
    :param: cmd [str] -- an sqlite3 command 
    :param: table_name [str] -- Title to display before the table is printed
    :param: curr [sqlite3.cursor] -- cursor in the db
    :param: args [tuple] -- any optional arguments to be passed to the cmd string
    """
    print(table_name)
    # find table
    if args == ():
        curr.execute(cmd)
    else:
        curr.execute(cmd, args)
    results = curr.fetchall()

    # get column names
    column_names = []
    for record in curr.description:
        column_names.append(record[0])

    max_column_width = 0
    
    # find max column width
    for i, column in enumerate(column_names):
        max_column_width = max(max_column_width, len(column))
        for result in results:
            max_column_width = max(max_column_width, len(str(result[i])))
    

    print_headers(column_names, max_column_width)
    
    # print the information for each table
    for record in results:
        for item in record:
            print('|{:<{width}}'.format(item, width=max_column_width), end='')
        print('|')
    
    print()

def print_headers(column_names, max_column_width):
    """
    Prints the headers for the table to be printed. used as a helper function in print_table()
    :param: column_names [list] -- the names of the columns
    :param: max_column_width [int] -- the width of the columns to be printed
    """
    for c in column_names:
        print('+{}'.format('=' * max_column_width), end='')
    print('+')

    for column in column_names:
        print('|{:^{width}}'.format(column.strip(), width=max_column_width), end='')
    print('|')

    for c in column_names:
        print('+{}'.format('=' * max_column_width), end='')
    print('+')

def print_all(curr):
    """
    prints all tables in db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    tables = """
    SELECT name FROM sqlite_master WHERE type = "table"
    """
    curr.execute(tables)

    for table in curr.fetchall():
        if table[0] != 'Players':
            cmd = """
            SELECT * FROM {}
            """.format(table[0])
            print_table(cmd, table[0], curr)
    
def connect(db_name):
    """
    Provides a connection to the sqlite3 database
    :param: db_name [str] -- name of the sqlite3 database to connect to
    """
    data_dir = Path.cwd() / Path('Files') / '{}'.format(db_name)
    conn = sql.connect(str(data_dir))
    curr = conn.cursor()
    return conn, curr