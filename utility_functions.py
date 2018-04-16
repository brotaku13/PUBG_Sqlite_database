import sqlite3 as sql
import table_creation
from pathlib import Path

def connect():
    """
    Provides a CONNection to the sqlite3 database
    :param: db_name [str] -- name of the sqlite3 database to CONNect to
    """
    path = Path(Path.cwd()) / Path("Files") / "pubg_game_db.sqlite3"
    conn = sql.connect(str(path))
    curr = conn.cursor()
    return conn, curr

CONN, CURR = connect()

def display_playerstats(*curr):
    cmd = """
    SELECT * FROM PlayerStats
    """
    return print_table(cmd, 'Display Player Stats')

def display_player_by_name(*curr):
    """
    Displays players by name
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT first_name, last_name FROM Players
    """
    return print_table(cmd, 'Display user by name')

def list_players(curr):
    """
    Displays all players
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    """
    return print_table(cmd, 'Display all Players')

def male_players(curr):
    """
    Displays all male players
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    WHERE gender='Male'
    """
    return print_table(cmd, 'Display all Male Players')

def female_players(curr):
    """
    Displays all female players
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT * FROM Players
    WHERE gender='Female'
    """
    return print_table(cmd, 'Display all female Players')

def list_events(curr):
    """
    Displays all events
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT round, event_id, game_number FROM Events
    """
    return print_table(cmd, 'Display all Events')

def players_by_event(curr):
    """
    Displays all players by event
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    records = list()

    cmd = """
    SELECT DISTINCT Players.user_id, Players.first_name, Players.last_name, Events.event_id, Events.round
    FROM Players JOIN Teams ON Players.user_id = Teams.user_id
    JOIN Events ON Teams.event_id = Events.event_id
    WHERE Events.round = 1;
    """
    records.append(print_table(cmd, 'Players by Event:Round 1'))

    cmd = """
    SELECT DISTINCT Players.user_id, Players.first_name, Players.last_name, Events.event_id, Events.round
    FROM Players JOIN Teams ON Players.user_id = Teams.user_id
    JOIN Events ON Teams.event_id = Events.event_id
    WHERE Events.round = 2;
    """
    records.append(print_table(cmd, 'Players by Event: Round 2'))

    cmd = """
    SELECT DISTINCT Players.user_id, Players.first_name, Players.last_name, Events.event_id, Events.round
    FROM Players JOIN Teams ON Players.user_id = Teams.user_id
    JOIN Events ON Teams.event_id = Events.event_id
    WHERE Events.round = 3;
    """
    records.append(print_table(cmd, 'Players by Event: Round 3'))

    return tuple(records)

def winners_by_event(*curr):   ##### TODO #####
    """
    Displays all winners of each event (uses award table)
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    cmd = """
    SELECT Awards.event_id, Awards.place, Awards.description, TeamScores.team_id, TeamScores.score
    FROM TeamScores JOIN Events ON TeamScores.event_id = Events.event_id
    JOIN Awards ON Awards.event_id = Events.event_id
    """
    return print_table(cmd, 'Winners by event')

def lookup_id(name: str, event: str, age: int, *curr):    ##### TODO ######
    """
    Looks up id by name, event, and age
    :param: name [str] -- first and last name of Player to look up
    :param: event [str] -- event the player participated in
    :param: age [int] -- age of player
    :param: CURR [sqlite3.cursor] -- cursor in the db
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
    return print_table(cmd, 'Display all Events', args=(first_name, last_name, age, event))

def delete_player_by_id(*curr):
    """
    removes a player from the player table.
    :param: CONN [sqlite3.CONNection] -- CONNection to the db
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    user_id = int(input('Enter the user id: '))
    cmd = """
    DELETE FROM Players WHERE user_id=?
    """
    CURR.execute(cmd, (user_id,))
    CONN.commit()

def update_player_by_id(*curr):
    """
    Updates player information
    :param: CONN [sqlite3.CONNection] -- CONNection to the db
    :param: CURR [sqlite3.cursor] -- cursor in the db
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
                CURR.execute(cmd, (user_id,))
                CONN.commit()
        except Exception as e:
            print('Please enter a valid number')
        
def player_info_by_id(curr):
    """
    Looks up Player information by player id: 
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    user_id = int(input('Lookup info by ID. Enter Player ID: '))
    cmd = """
    SELECT * from Players
    WHERE user_id=?
    """
    print_table(cmd, 'Player id '.format(user_id), curr)

def player_stats_by_id(curr):
    """
    Looks up player stats by player id
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    user_id = int(input('Lookup info by ID. Enter Player ID: '))
    cmd = """
    SELECT * FROM PlayerStats WHERE user_id=?
    """
    curr.execute(cmd, (user_id,))

def player_awards_by_id(curr):   ##### TODO #####
    """
    Prints out the awards of a given player. If they did not place, instead of printing out the table, it prints the message " did not win anything..."
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    user_id = int(input('Lookup info by ID. Enter Player ID: '))
    cmd = """
    SELECT * FROM Awards WHERE user_id=?
    """


def run_all(curr, conn):
    """
    Runs all necessary functions. mostly used for utility and testing
    :param: CONN [sqlite3.CONNection] -- CONNection to the db
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    return display_player_by_name(), list_players(), male_players(), female_players(), list_events()

def print_table(cmd, table_name, *curr, args=()):
    """
    Prints a table in a readable format
    :param: cmd [str] -- an sqlite3 command
    :param: table_name [str] -- Title to display before the table is printed
    :param: CURR [sqlite3.cursor] -- cursor in the db
    :param: args [tuple] -- any optional arguments to be passed to the cmd string
    """

    # find table
    if args == ():
        CURR.execute(cmd)
    else:
        CURR.execute(cmd, args)
    results = CURR.fetchall()
    print('{} -- {} items'.format(table_name, len(results)))

    # get column names
    column_names = []
    for record in CURR.description:
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

def print_all(*curr):
    """
    prints all tables in db
    :param: CURR [sqlite3.cursor] -- cursor in the db
    """
    tables = """
    SELECT name FROM sqlite_master WHERE type = "table"
    """
    CURR.execute(tables)

    for table in CURR.fetchall():
        if table[0] != 'Players':
            cmd = """
            SELECT * FROM {}
            """.format(table[0])
            print_table(cmd, table[0])
