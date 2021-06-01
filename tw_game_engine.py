from random import randint
from tw_player import Player
from tw_player_ai import Player as AI

class GameEngine:
    def __init__(self):
        self.on_start()
        # we want to keep a list of 'registered' players
        # this is so we can distinguish between 'real' players, and npc / ai players
        self.registered_players = []

    def on_start(self):
        # we store all players in a dictionary
        # player_id : Player object
        players_dict = {}
        # setting up AI players
        ai_1 =  str(randint(0, 64000))
        ai_2 =  str(randint(0, 64000))
        players_dict[ai_1] = AI(ai_1, (100,100), 0)
        players_dict[ai_2] = AI(ai_2, (300,300), 0)
        ###
        self.loads(players_dict)

    def loads(self, data):
        self.player_dict = data

    def add_player(self, id):
        self.player_dict[id] = Player(id, (250,250), 0)
        self.registered_players.append(id)

    def move_ai(self):
        for id in self.player_dict:
            if id not in self.registered_players:
                self.player_dict[id].move()

    def move_player(self, id, keys):
        self.player_dict[id].move(keys)

    def update_objects(self):
        # we don't want to send the whole player object on each network broadcast
        # so we create a temporary dictionary that the client can use to render the scene
        data_dict = {}
        for id in self.player_dict:
            pos = (self.player_dict[id].x, self.player_dict[id].y)
            dir = self.player_dict[id].dir
            data = [pos, dir]
            data_dict[id] = data
        return data_dict