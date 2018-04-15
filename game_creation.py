import sqlite3 as sq
from pathlib import Path
import random
import table_creation
import utility_functions

class Player:
    num_players = 0   # total players in game
    max_distance = 300  #m ax distance traveled per turn
    player_health = 200  #total player health
    probability_shoot = 4 #  1/x
    probability_kill = 6  # 1/x
    probability_headshot = 2  # 1/x
    alive_players = []  #list of players still alive
    time_elapsed = 0  # in seconds

    #points
    HEADSHOT = 100

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.kills = 0
        self.damage = 0
        self.distance = 0
        self.headshots = 0
        self.time = 0
        self.died = 0  # bit: 1 = died, 0 = alive
        self.time = 0
        self.score = 0

        Player.num_players += 1
        Player.alive_players.append(self)

    def __travel(self):
        """
        Moves player some random distance between one and Player.max_distance
        """
        d = random.randint(1, Player.max_distance)
        self.distance += d
        self.score += d
        #print('User {} traveled {}m'.format(self.user_id, d))

    def __kill(self):
        """
        Increments kills and removes a player from the Player.alive_players list. Some small chance to land a headshot
        """
        self.kills += 1
        headshot = 'no'
        if random.randint(1, Player.probability_headshot) == 1:
            headshot = 'yes'
            self.headshots += 1
            self.score += Player.HEADSHOT

        d = random.randint(1, Player.player_health)
        self.damage += d
        self.score += d

        Player.num_players -= 1
        killed = random.choice(Player.alive_players)
        killed.died = 1
        killed.time = Player.time_elapsed
        Player.alive_players.pop(Player.alive_players.index(killed))

        # print('User {} killed user {}. Headshot: {}, Damage: {}, Total kills: {}'.format(
        #     self.user_id,
        #     killed.user_id,
        #     headshot,
        #     d,
        #     self.kills))

    def __shoot(self):
        """
        The Player shoots. they have some small chance to kill defined by Player.probability_kill, otherwise, they just do damage
        """
        if random.randint(1, Player.probability_kill) == 1 and self.num_players > 1:
            self.__kill()
        else:
            d = random.randint(1, Player.player_health - 1)
            self.damage += d
            #print('User {} did {} damage'.format(self.user_id, d))

    def take_turn(self):
        """
        Allows the player to take a turn. They can either travel, or shoot
        """
        if random.randint(1, Player.probability_shoot) == 1:
            self.__shoot()
        else:
            self.__travel()

    def stats(self):
        """
        returns stats for the player minus the user_id
        """
        return [self.kills, self.damage, self.distance, self.headshots, self.time, self.died, self.score]

    def __str__(self):
        return f'User_id: {self.user_id}, Kills: {self.kills}, Damage: {self.damage}, Distance: {self.distance}, Headshots: {self.headshots}, Time: {self.time}, Died: {self.died}, Score: {self.score}'

class Game:
    minimum_turn_len = 30
    maximum_turn_len = 100
    team_id = 1

    def __init__(self, num_teams, event_id, players, connection, cursor):
        self._num_teams = num_teams
        self._players_per_team = 100 / self._num_teams
        self._event_id = event_id
        self._players = players
        self._teams = {}  # team_id: [list of Players()]
        self._conn = connection
        self._curr = cursor
        self.__form_teams(players)

    def __form_teams(self, player_records):
        """
        Forms teams based on the number of teams and the Player table in the db
        :param: player_records [list] -- list of 1-tuples holding the player-ids
        """
        try:
            if Game.team_id > self._num_teams * 3:
                for player in player_records:
                    # all three games in round one have taken place, need to find team ID from team table
                    user_id = player[0]
                    cteam_id = player[1]

                    insert = """
                    INSERT INTO Teams(team_id, user_id, event_id)
                    VALUES(?, ?, ?)
                    """
                    try:
                        self._curr.execute(insert, (cteam_id, user_id, self._event_id))
                    except Exception as e:
                        print(e)
                    self._conn.commit()

                    if cteam_id in self._teams:
                        self._teams[cteam_id].append(Player(user_id))
                    else:
                        self._teams[cteam_id] = [Player(user_id)]
            else:
                jump = int(100 / self._num_teams)
                for i in range(0, len(player_records), jump):
                    for j in range(jump):
                        user_id = player_records[i + j][0]
                        insert = """
                        INSERT INTO Teams(team_id, user_id, event_id)
                        VALUES(?, ?, ?) 
                        """
                        self._curr.execute(insert, (Game.team_id, user_id, self._event_id))
                        self._conn.commit()
                        if Game.team_id in self._teams:
                            self._teams[Game.team_id].append(Player(user_id))
                        else:
                            self._teams[Game.team_id] = [Player(user_id)]

                    Game.team_id += 1
        except sq.IntegrityError as e:
            print(str(e))
            path = Path(Path.cwd()) / Path("Files") / Path("pubg_game_db.sqlite3")
            if path.exists():
                path.unlink()
            return

    def reset_player_class(self):
        Player.num_players = 0
        Player.alive_players = []
        Player.time_elapsed = 0

    def play_game(self):
        """
        plays one game. Continues until only one player is left standing.
        """
        turns = 0
        while Player.num_players > 1:
            Player.time_elapsed += random.randint(Game.minimum_turn_len, Game.maximum_turn_len)

            for t_id, player_list in self._teams.items():
                for player in player_list:
                    if player in Player.alive_players:
                        player.take_turn()
            turns += 1

        Player.alive_players[0].time = Player.time_elapsed   # update final player with the full elapsed time
        #self.print_game_outcome(turns)
        self.record_stats()
        self.reset_player_class()

    def print_game_outcome(self, turns):
        """
        Convenience funtion for printing the game outcome and player stats
        """
        print('Total Turns: ', turns)
        for t_id, player_list in self._teams.items():
            print(f'Team: {t_id}')
            for player in player_list:
                print('\t', player)

    def record_stats(self):
        """
        records the stats from each player object into the PlayerStats table
        """
        for t_id, player_list in self._teams.items():
            for player in player_list:
                cmd = """
                INSERT INTO PlayerStats(user_id, event_id, team_id, kills, damage, distance, headshots, time, death, score)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                values = [player.user_id, self._event_id, t_id]
                values += player.stats()
                self._curr.execute(cmd, tuple(values))

    def update_awards(self):
        """
        TODO
        """
        pass

def new_game(event_id, num_teams, players, curr, conn):
    """
    creates and initializes a new game.
    :param: event_id [int] -- event id of the event the game is being run for
    :param: num_teams [int] -- number of teams total, should be an equal divisor of 100
    :param: players [list] -- list of player information of players participating in this game
    """
    game = Game(num_teams, event_id, players, conn, curr)
    game.play_game()