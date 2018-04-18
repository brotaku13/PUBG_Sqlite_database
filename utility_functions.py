import sqlite3 as sql
import table_creation
from pathlib import Path

def connect():
    """
    Provides a connection to the sqlite3 database
    :param: db_name [str] -- name of the sqlite3 database to connect to
    """
    path = Path(Path.cwd()) / Path("Files") / "pubg_game_db.sqlite3"
    conn = sql.connect(str(path))
    curr = conn.cursor()
    return conn, curr

def display_playerstats(curr):
    cmd = """
    SELECT * FROM PlayerStats
    """
    print_table(cmd, 'Display Player Stats', curr)

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
    LIMIT 300
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
    SELECT event_id, event_name, round, game_number FROM Events
    """
    print_table(cmd, 'Display all Events', curr)

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
    SELECT Awards.event_id, Awards.place, Awards.description, Awards.team_id, TeamScores.score
    FROM TeamScores JOIN Awards ON TeamScores.team_id = Awards.team_id
    WHERE TeamScores.event_id = 6
    """
    print_table(cmd, 'Winners', curr)

def lookup_id(name: str, event: int, age: int, curr):    ##### TODO ######
    """
    Looks up id by name, event, and age
    :param: name [str] -- first and last name of Player to look up
    :param: event [int] -- event the player participated in
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
    print_table(cmd, 'Display Player ID', curr, args=(first_name, last_name, age, event))

def delete_player_by_id(conn, curr):
    """
    Runs all necessary functions. mostly used for utility and testing
    removes a player from the player table.
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    while True:
        try:
            user_id = int(input('Enter the user id: '))
            break
        except ValueError:
            print('Please enter an ID which is a number')

    check = """
    select user_id, first_name, last_name from players
    where user_id=?
    """
    curr.execute(check, (user_id,))
    records = curr.fetchall()
    if len(records) == 0:
        print("Invalid User.")
    else:
        print_table(check, 'The User to be deleted', curr, args=(user_id,))

        while True:
            try:
                choice = str(input('Is this the correct user? y/n ')).lower()
                if choice != 'n' and choice != 'y':
                    raise ValueError
                else:
                    if choice == 'y':
                        cmd = """
                        DELETE FROM Players WHERE user_id=?
                        """
                        curr.execute(cmd, (user_id,))
                        conn.commit()
                        return
                    else:
                        print('Returning to menu')
                        return

            except ValueError:
                print('Please enter y/n')

def get_user(curr):
    user_id = 0
    while True:
        while True:
            try:
                user_id = int(input('Enter user id: '))
                break
            except:
                print('Please enter a correct value')
        check = """
        select user_id,username, first_name, last_name, gender, phone, age from players
        where user_id=?
        """
        curr.execute(check, (user_id,))
        records = curr.fetchall()
        for rec in records:
            if rec[1] != "":
                print_table(check, 'The User to be changed', curr, args=(user_id,))
                while True:
                    try:
                        choice = str(input('Is this the correct user? y/n')).lower()
                        if choice != 'n' and choice != 'y':
                            raise ValueError
                        else:
                            if choice == 'y':
                                return user_id
                            else:
                                break
                    except:
                        print('Please enter y or n')
        if len(records) == 0:
            print("Invalid entry.")

def update_player_by_id(conn, curr):
    """
    Updates player information
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    user_id = get_user(curr)
    menu = """
    Which Attribute would you like to change?
        1. Username
        2. First Name
        3. Last Name
        4. Phone
        5. Gender
        6. Age
        7. Finish
    """

    while True:
        print(menu)
        try:
            choice = int(input('Attribute: '))
            if choice < 1 or choice > 7:
                raise ValueError('Bad choice')
            else:
                attribute_change = ''
                if choice == 1:
                    attribute_change = 'username="{}"'.format(input('New Username: '))
                elif choice == 2:
                    attribute_change = 'first_name="{}"'.format(input('New First Name: '))
                elif choice == 3:
                    attribute_change = 'last_name="{}"'.format(input('New Last Name: '))
                elif choice == 4:
                    num = int(input('New Phone (###-###-####)').replace('-', ''))
                    while num < 1000000000 or num > 9999999999:
                        num = int(input("Please input a valid number: ").replace('-', ''))
                    attribute_change = 'phone={}'.format(num)
                elif choice == 5:
                    attribute_change = 'gender="{}"'.format(input('New Gender (Male / Female / *Anything you want*)').title())
                elif choice == 6:
                    age = int(input('New Age (>18)'))
                    while age < 18:
                        age = int(input('Please change your age to above 18: '))
                    attribute_change = 'age={}'.format(age)
                else:
                    break

                cmd = """
                UPDATE Players
                SET {}
                WHERE user_id=?
                """.format(attribute_change)
                curr.execute(cmd, (user_id,))
                conn.commit()
                show_change = """
                select user_id,username, first_name, last_name, gender, phone, age from players
                where user_id=?
                """
                print_table(show_change, 'Modified user', curr, args=(user_id,))

        except ValueError:
            print('Please enter a valid number')
        except Exception as e:
            print(str(e))
        
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

def player_stats_by_all(curr):
    """
    """
    cmd = """
    SELECT * FROM PlayerStats
    """
    print_table(cmd, "All Player Stats", curr)

def player_stats_by_event_id(curr):
    """
    """
    event = input("Which event are you looking up? ")
    while int(event) < 1 or int(event) > 6:
        event = input("Enter an event 1-6: ")
    cmd = """
    SELECT * FROM PlayerStats WHERE event_id=?
    """
    print_table(cmd, "Player Stats EVENT {}".format(event), curr, args=(event,))

def player_stats_by_top_scores(curr):
    """
    """
    event = input("Which event are you looking up? ")
    while int(event) < 1 or int(event) > 6:
        event = input("Enter an event 1-6: ")
    cmd = """
    SELECT * FROM PlayerStats WHERE event_id=? ORDER BY score DESC LIMIT 10
    """
    print_table(cmd, "Top 10 Player Stats EVENT {}".format(event), curr, args=(event,))

def player_stats_by_finals(curr):
    """
    """
    cmd = """
    SELECT * FROM PlayerStats WHERE event_id=6 ORDER BY score DESC
    """
    print_table(cmd, "FINALISTS", curr)
        
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