import game_creation
import utility_functions
import table_creation

def run_games(curr, conn):
    """
    Runs all games for each event. In this version, alll players play every event, but this may have to be changed
    :param: conn [sqlite3.connection] -- connection to the db
    :param: curr [sqlite3.cursor] -- cursor in the db
    """
    get_events = """
    SELECT event_id, num_teams FROM Events
    """
    events = curr.execute(get_events).fetchall()
    for event in events:
        game_creation.new_game(event[0], event[1], curr, conn)



def main():
    # get connection
    conn, curr = utility_functions.connect('pubg_game_db.sqlite3')

    # list all events and the team numbers associated with each event
    events = [('ErangelSolo', 100), ('ErangelDuo', 50), ('ErangelSquad', 25)]

    # create the tables
    table_creation.create_tables(events, curr, conn)

    # run the games
    run_games(curr, conn)

    # run all utility functions (so far)
    utility_functions.run_all(curr, conn)

    # close the connection
    conn.close()

if __name__ == '__main__':
    main()