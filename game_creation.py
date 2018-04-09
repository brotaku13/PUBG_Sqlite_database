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
        self.__num_teams = num_teams
        self.__players_per_team = 100 / self.__num_teams
        self.__event_id = event_id
        self.__players = players
        self.__teams = {}  # team_id: [list of Players()]
        self.__conn = connection
        self.__curr = cursor
        self.__form_teams(players)

    def __form_teams(self, player_records):
        """
        Forms teams based on the number of teams and the Player table in the db
        """

        for player in player_records:
            user_id = player[0]
            # check to see if first round has happened, if so, then the players must use the team_id's from the previous rounds
            if Game.team_id > self.__num_teams * 3:
                #all three rounds have taken place, need to find team ID from team table
                find_id = """
                SELECT team_id FROM Teams
                WHERE user_id=?
                """
                self.__curr.execute(find_id, (user_id,))
                team_records = self.__curr.fetchall()

                insert = """
                INSERT INTO Teams(team_id, user_id, event_id)
                VALUES(?, ?, ?)
                """
                continuing_team_id = team_records[0][0]
                self.__curr.execute(insert, (continuing_team_id, user_id, self.__event_id))
                self.__conn.commit()

                if continuing_team_id in self.__teams:
                    self.__teams[continuing_team_id].append(Player(user_id))
                else:
                    self.__teams[continuing_team_id] = [Player(user_id)]
            else:
                # three rounds have not taken place, so use the static id
                insert = """
                INSERT INTO Teams(team_id, user_id, event_id)
                VALUES(?, ?, ?)
                """
                self.__curr.execute(insert, (Game.team_id, user_id, self.__event_id))
                self.__conn.commit()
                if Game.team_id in self.__teams:
                    self.__teams[Game.team_id].append(Player(user_id))
                else:
                    self.__teams[Game.team_id] = [Player(user_id)]

                Game.team_id += 1

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

            for t_id, player_list in self.__teams.items():
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
        for t_id, player_list in self.__teams.items():
            print(f'Team: {t_id}')
            for player in player_list:
                print('\t', player)
        
    def record_stats(self):
        """
        records the stats from each player object into the PlayerStats table
        """
        for t_id, player_list in self.__teams.items():
            for player in player_list:
                cmd = """
                INSERT INTO PlayerStats(user_id, event_id, team_id, kills, damage, distance, headshots, time, death, score)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                values = [player.user_id, self.__event_id, t_id]
                values += player.stats()
                self.__curr.execute(cmd, tuple(values))

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