import sqlite3 as sql
from pathlib import Path


def drop_table(table_name, curr, conn):
    drop = """
    DROP TABLE IF EXISTS {}
    """.format(table_name)
    curr.execute(drop)
    conn.commit()
    
def create_tables(game_map: str, game_type: str, conn, curr):
    
    event_name = f'{game_map}{game_type}'
    drop_table(event_name, curr, conn)
    #create duo team makeup
        # team #, player, primary key (Team#Player)
    team_makeup_table_name = f'{event_name}TeamMakeup'
    create_team_makeup = """
    CREATE TABLE {}(
        team_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        PRIMARY KEY (team_id, username)
    )
    """.format(team_makeup_table_name)
    curr.execute(create_team_makeup)
    conn.commit()

    for i in range(1,4):
        team_round_stats_name = f'{event_name}TeamStatsRound{i}'
        player_round_stats_name = f'{event_name}PlayerStatsRound{i}'
        drop_table(team_round_stats_name, curr, conn)
        drop_table(player_round_stats_name, curr, conn)
        
        # duo team stats for each round
        create_team_stats_round = """
        CREATE TABLE {}(
            team_id INTEGER PRIMARY KEY NOT NULL,
            kills INTEGER NOT NULL,
            damage INTEGER NOT NULL,
            distance INTEGER NOT NULL,
            win INTEGER NOT NULL,
            headshots INTEGER NOT NULL,
            time INTEGER NOT NULL
        )
        """.format(team_round_stats_name)

        curr.execute(create_team_stats_round)
        conn.commit()
        

        create_player_stats_round = """
        CREATE TABLE {}(
            username TEXT PRIMARY KEY NOT NULL,
            kills INTEGER NOT NULL,
            damage INTEGER NOT NULL,
            distance INTEGER NOT NULL,
            headshots INTEGER NOT NULL,
            time INTEGER NOT NULL
        )
        """.format(player_round_stats_name)

        curr.execute(create_player_stats_round)
        conn.commit()
        
    #create total team stats
    team_total_stats_name = f'{event_name}TeamStats'
    drop_table(team_total_stats_name, curr, conn)

    create_total_team_stats = """
    CREATE TABLE {}(
        team_id INTEGER PRIMARY KEY NOT NULL,
        kd REAL NOT NULL,
        damage INTEGER NOT NULL,
        win_percentage REAL NOT NULL,
        headshot_percentage REAL NOT NULL,
        average_time INTEGER NOT NULL,
        most_kills INTEGER NOT NULL,
        total_distance INTEGER NOT NULL
    )
    """.format(team_total_stats_name)

    curr.execute(create_total_team_stats)
    conn.commit()

def connect(db_name):
    data_dir = Path.cwd() / Path('Files') / '{}'.format(db_name)
    conn = sql.connect(str(data_dir))
    curr = conn.cursor()
    return conn, curr

def create_game():
    maps = ['Erangel', 'Miramar', 'Savage']
    game_types = ['Solo', 'Duo', 'Squad']
    conn, curr = connect('pubg_game_db.sqlite3')
    for game_map in maps:
        for game_type in game_types:
            create_tables(game_map, game_type, conn, curr)

create_game()