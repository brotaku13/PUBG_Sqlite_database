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
    return print_table(cmd, 'Display user by name', curr)


def list_players(curr):
    """
    Displays all players
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    """
    return print_table(cmd, 'Display all Players', curr)


def male_players(curr):
    """
    Displays all male players
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    WHERE gender='Male'
    """
    return print_table(cmd, 'Display all Male Players', curr)


def female_players(curr):
    """
    Displays all female players
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    WHERE gender='Female'
    """
    return print_table(cmd, 'Display all female Players', curr)


def list_events(curr):
    """
    Displays all events
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT round, event_id, game_number FROM Events
    """
    return print_table(cmd, 'Display all Events', curr)


def players_by_event(curr):
    """
    Displays all players by event
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    records = list()

    cmd = """
    SELECT DISTINCT Players.user_id, Players.first_name, Players.last_name, Events.event_id, Events.round
    FROM Players JOIN Teams ON Players.user_id = Teams.user_id
    JOIN Events ON Teams.event_id = Events.event_id
    WHERE Events.round = 1;
    """
    records.append(print_table(cmd, 'Players by Event:Round 1', curr))

    cmd = """
    SELECT DISTINCT Players.user_id, Players.first_name, Players.last_name, Events.event_id, Events.round
    FROM Players JOIN Teams ON Players.user_id = Teams.user_id
    JOIN Events ON Teams.event_id = Events.event_id
    WHERE Events.round = 2;
    """
    records.append(print_table(cmd, 'Players by Event: Round 2', curr))

    cmd = """
    SELECT DISTINCT Players.user_id, Players.first_name, Players.last_name, Events.event_id, Events.round
    FROM Players JOIN Teams ON Players.user_id = Teams.user_id
    JOIN Events ON Teams.event_id = Events.event_id
    WHERE Events.round = 3;
    """
    records.append(print_table(cmd, 'Players by Event: Round 3', curr))

    return tuple(records)

def winners_by_event(curr):   ##### TODO #####
    """
    Displays all winners of each event (uses award table)
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT Awards.event_id, Awards.place, Awards.description, TeamScores.team_id, TeamScores.score
    FROM TeamScores JOIN Events ON TeamScores.event_id = Events.event_id
    JOIN Awards ON Awards.event_id = Events.event_id
    """
    return print_table(cmd, 'Winners by event', curr)

def lookup_id(name: str, event: str, age: int, curr):    ##### TODO ######
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
        SELECT event_id FROM Events
        )
    """
    return print_table(cmd, 'Display all Events', curr, args=(first_name, last_name, age, event))

def delete_player_by_id(conn, curr):
    """
    removes a player from the player table.
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    user_id = int(input('Enter the user id: '))
    cmd = """
    DELETE FROM Players WHERE user_id=?
    """
    curr.execute(cmd, (user_id,))
    conn.commit()

def update_player_by_id(conn, curr):
    """
    Updates player information
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    user_id = int(input('Enter user id: '))
    while True:
        print('Which Attribute would you like to change? ')
        print('1. Username')
        print('2. First Name')
        print('3. Last Name')
        print('4. Phone')
        print('5. Gender')
        print('6. Age')
        print('7. Quit')
        try:
            choice = int(input('Attribute: '))
            if choice < 1 or choice > 7:
                raise ValueError('Bad choice')
            else:
                attribute_change = ''
                if choice == 1:
                    attribute_change = 'username={}'.format(input('New Username: '))
                elif choice == 2:
                    attribute_change = 'first_name={}'.format(input('New First Name: '))
                elif choice == 3:
                    attribute_change = 'last_name={}'.format(input('New Last Name: '))
                elif choice == 4:
                    attribute_change = 'phone={}'.format(int(input('New Phone (###-###-####)').replace('-', '')))
                elif choice == 5:
                    attribute_change = 'gender={}'.format(input('New Gender (Male / Female)').title())
                elif choice == 6:
                    attribute_change = 'age={}'.format(int(input('New Age (>18)')))
                else:
                    break

                cmd = """
                UPDATE Players
                SET {}
                WHERE user_id=?
                """.format(attribute_change)
                curr.execute(cmd, (user_id,))
                conn.commit()
        except Exception as e:
            print('Please enter a valid number')

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

    # find table
    if args == ():
        curr.execute(cmd)
    else:
        curr.execute(cmd, args)
    results = curr.fetchall()
    print('{} -- {} items'.format(table_name, len(results)))

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

    return results

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