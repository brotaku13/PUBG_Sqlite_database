import game_creation
import utility_functions
import table_creation
import game_creation
import graph
import subprocess as sub
from pathlib import Path
import test

TIMEOUT = 3


def update_scores(event_id, curr, conn):
    """
    Updates the scores for a specific event. If it does not
    exist, it adds the information into TeamScores. Or else
    It updates the existing score to the new score.

    event_id: int, The id number of the competition event.
    curr: cursor, Allows Python code to execute sqlite code
    conn: connection, Read-only attribute returning a reference to the connection.
    """
    find_team_ids = """
    SELECT team_id, score FROM PlayerStats
    WHERE event_id=?
    """
    curr.execute(find_team_ids, (event_id,))
    team_scores = curr.fetchall()
    for item in team_scores:
        team_id = item[0]
        new_score = item[1]
        ## if team not already in team scores, insert
        find_team_score = """
        SELECT * FROM TeamScores
        WHERE team_id=? AND event_id=?
        """
        curr.execute(find_team_score, (team_id, event_id))
        existing = curr.fetchall()
        if len(existing) == 0:
            # no records exist for this team, must insert new record
            insert = """
            INSERT INTO TeamScores(team_id, event_id, score)
            VALUES(?, ?, ?)
            """
            curr.execute(insert, (team_id, event_id, new_score))
            conn.commit()

        else:
            ## if team already in scores, then update
            old_score = existing[0][2]
            update = """
            UPDATE TeamScores
            SET score=?
            WHERE team_id=? AND event_id=?
            """
            curr.execute(update, (old_score + new_score,team_id, event_id))

def run_competition(event, conn, curr):
    """
    Runs the competition event based on the event. It
    utilizes all other functions.

    event: list, The event information needed to run the competition [event name, number of teams]
    curr: cursor, Allows Python code to execute sqlite code
    conn: connection, Read-only attribute returning a reference to the connection.
    """
    event_name = event[0]
    num_teams = event[1]
    # get events for the competition
    find_event_rounds = """
    SELECT * FROM Events
    WHERE event_name=?
    """
    curr.execute(find_event_rounds, (event_name,))
    events_list = curr.fetchall()

    user_id_min = 1
    user_id_max = 100

    ####################################round 1
    for event in events_list[0:3]:
        event_id = event[0]

        select_players = """
        SELECT user_id FROM Players
        WHERE user_id >= ? AND user_id <= ?
        """
        curr.execute(select_players, (user_id_min, user_id_max))
        players = curr.fetchall()

        game_creation.new_game(event_id, num_teams, players, curr, conn)

        user_id_min += 100
        user_id_max += 100

        update_scores(event_id, curr, conn)

    #utility_functions.print_table("SELECT * FROM PlayerStats", 'Player scores after 3 rounds', curr)

    ################# round 2
    for event in events_list[3:5]:
        # grab top 200 from playerstats
        event_id = event[0]
        num_teams = event[4]

        if event[3] == 1:  # if game_number == 1
            top_teams = """
            SELECT user_id, team_id FROM Teams
            WHERE team_id IN (
                SELECT team_id FROM TeamScores
                WHERE event_id IN (
                    SELECT event_id FROM Events
                    WHERE event_name=? AND round=1
                )
                ORDER BY score DESC
                LIMIT ?
            )
            """
           # utility_functions.print_table(top_teams, 'after round 1 -- top half of top 50', curr, args=(event_name, num_teams))
            curr.execute(top_teams, (event_name,num_teams))

        else:
            top_teams = """
            SELECT user_id, team_id FROM Teams
            WHERE team_id IN (
                SELECT team_id FROM TeamScores
                WHERE event_id IN (
                    SELECT event_id FROM Events
                    WHERE event_name=? AND round=1
                )
                ORDER BY score DESC
                LIMIT ? OFFSET ?
            )
            """
           # utility_functions.print_table(top_teams, 'after round 1 -- bottom half of top 200', curr, args=(event_name, num_teams, num_teams))

            curr.execute(top_teams, (event_name,num_teams, num_teams))

        players = curr.fetchall()

        game_creation.new_game(event_id, num_teams, players, curr, conn)
        update_scores(event_id, curr, conn)

    ############################################# round 3
    finalists = """
    SELECT DISTINCT user_id, team_id FROM Teams
    WHERE team_id IN (
        SELECT team_id FROM TeamScores
        WHERE event_id IN (
            SELECT event_id FROM Events
            WHERE event_name=? AND round = 2
        )
        ORDER BY score DESC LIMIT ?
    )

    """
   # utility_functions.print_table(finalists, 'Finalists, top 100 from round 2', curr, args=(event_name, num_teams))

    curr.execute(finalists, (event_name, num_teams))
    players = curr.fetchall()


    find_event_info = """
    SELECT * FROM Events WHERE event_name=? AND round=?
    """
    curr.execute(find_event_info, (event_name, 3))
    final_event_info = curr.fetchall()
    event_id = final_event_info[0][0]

    game_creation.new_game(event_id, num_teams, players, curr, conn)
    update_scores(event_id, curr, conn)

    finalists = """
    SELECT team_id FROM PlayerStats
    WHERE event_id=6
    ORDER BY score DESC LIMIT 3
    """
    curr.execute(finalists)
    winners = curr.fetchall()

    for place, team in enumerate(winners):
        insert = """
        UPDATE Awards
        SET team_id=?
        WHERE place=?
        """
        place_text = ''
        if place == 0:
            place_text = 'First'
        elif place == 1:
            place_text = 'Second'
        elif place == 2:
            place_text = 'Third'
        curr.execute(insert, (team[0], place_text))
        conn.commit()


def main_code(conn, curr, num_teams):
    # list all events and the team numbers associated with each event
    events = [('ErangelSolo', num_teams)]
    awards = [{'First': '$5000', 'Second': '$2500', 'Third': '$1000'}]

    ### comment this portion to stop from recreating the whole database every single time #####
    #######    so that you can test the required functions         ##########
    table_creation.create_tables(events, awards, conn, curr)

    for event in events:
        run_competition(event, conn, curr)
        game_creation.Game.team_id = 1

