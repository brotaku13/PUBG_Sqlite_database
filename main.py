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

def update_scores(event_id, curr, conn):
    find_team_ids = """
    SELECT team_id, score FROM PlayerStats
    WHERE event_id=?
    """
    curr.execute(find_team_ids, (event_id,))
    team_scores = curr.fetchall()
    for item in team_scores:
        team_id = item[0]
        score = item[1]
        # no records exist for this team, must insert new record
        insert = """
        INSERT INTO TeamScores(team_id, event_id, score)
        VALUES(?, ?, ?)
        """
        curr.execute(insert, (team_id, event_id, score))
        conn.commit()

            
def run_competition(event, curr, conn):
    event_name = event[0]
    # get events for the competition
    find_event_rounds = """
    SELECT * FROM Events
    WHERE event_name=?
    """
    curr.execute(find_event_rounds, (event_name,))
    events_list = curr.fetchall()

    user_id_min = 1
    user_id_max = 100
    

    #round 1
    for event in events_list[0:3]:
        event_id = event[0]
        num_teams = event[4]

        select_players = """
        SELECT * FROM Players
        WHERE user_id >= ? AND user_id <= ?
        """
        curr.execute(select_players, (user_id_min, user_id_max))
        players = curr.fetchall()

        game_creation.new_game(event_id, num_teams, players, curr, conn)

        user_id_min += 100
        user_id_max += 100

        update_scores(event_id, curr, conn)
    
    utility_functions.print_table("SELECT * FROM PlayerStats", 'Player scores after 3 rounds', curr)


    ################# round 2
    for event in events_list[3:5]:
        # grab top 200 from playerstats
        event_id = event[0]
        num_teams = event[4]

        if event[3] == 1:  # if game_number == 1
            top_teams = """
            SELECT * FROM Players
            WHERE user_id IN(
                SELECT user_id FROM Teams
                WHERE team_id IN (
                    SELECT team_id FROM TeamScores
                    WHERE event_id IN (
                        SELECT event_id FROM Events
                        WHERE event_name=? AND round=1
                    )
                    ORDER BY score DESC LIMIT 100
                )
            )
            """
            utility_functions.print_table(top_teams, 'after round 1 -- top half of top 200', curr, args=(event_name,))
        else:
            top_teams = """
            SELECT * FROM Players
            WHERE user_id IN(
                SELECT user_id FROM Teams
                WHERE team_id IN (
                    SELECT team_id FROM TeamScores
                    WHERE event_id IN (
                        SELECT event_id FROM Events
                        WHERE event_name=? AND round=1
                    )
                    ORDER BY score DESC LIMIT 100 OFFSET 100
                )
            )
            """
            utility_functions.print_table(top_teams, 'after round 1 -- bottom half of top 200', curr, args=(event_name,))

        curr.execute(top_teams, (event_name,))
        players = curr.fetchall()

        game_creation.new_game(event_id, num_teams, players, curr, conn)
        update_scores(event_id, curr, conn)

    ########### round 3
    top_100 = """
    SELECT * FROM Players
    WHERE user_id IN(
        SELECT user_id FROM Teams
        WHERE team_id IN (
            SELECT team_id FROM TeamScores
            WHERE event_id IN (
                SELECT event_id FROM Events
                WHERE event_name=? AND round=2
            )
            ORDER BY score DESC LIMIT 100 OFFSET 100
        )
    )
    """
    utility_functions.print_table(top_100, 'Finalists,  top 100 from round 2', curr, args=(event_name,))
    curr.execute(top_100, (event_name,))
    players = curr.fetchall()
    
    ## this needs to be generalized
    event = events_list[5]
    event_id = event[0]
    num_teams = event[4]

    game_creation.new_game(event_id, num_teams, players, curr, conn)
    update_scores(event_id, curr, conn)

    finalists = """
    SELECT * FROM PlayerStats
    WHERE event_id=6
    """
    utility_functions.print_table(finalists, 'Top 100 FINALISTS', curr)
    #utility_functions.print_table('SELECT * FROM TeamScores', 'teamScores', curr)

def main():
    # get connection
    conn, curr = utility_functions.connect('pubg_game_db.sqlite3')

    # list all events and the team numbers associated with each event
    events = [('ErangelSolo', 100)]

    # create the tables
    table_creation.create_tables(events, curr, conn)

    players_used = 0
    #run competition
    for event in events:
        run_competition(event, curr, conn)

    # run all utility functions (so far)
    #utility_functions.run_all(curr, conn)

    # close the connection
    conn.close()

if __name__ == '__main__':
    main()