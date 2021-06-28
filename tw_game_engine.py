import pygame
from random import randint
from tw_char import Player, NPC
from tw_c import GAME_TICK

class GameEngine:
    def __init__(self):
        self.on_start()
        # we want to keep a list of 'registered' players
        # this is so we can distinguish between 'real' players, and npc / ai players
        self.registered_players = []

    def on_start(self):
        # we store all players (including npc/ai) in a dictionary
        # player_id : Player object
        players_dict = {}
        # setting up AI players
        ai_1 =  str(randint(0, 64000))
        ai_2 =  str(randint(0, 64000))
        players_dict[ai_1] = NPC(ai_1, (100,100), 0)
        players_dict[ai_2] = NPC(ai_2, (300,300), 0)
        self.loads(players_dict)
        self.prepare_send_object()

    def loads(self, data):
        self.player_dict = data

    def add_player(self, id):
        self.player_dict[id] = Player(id, (250,250), 0)
        self.registered_players.append(id)

    def move_npc(self):
        for id in self.player_dict:
            if id not in self.registered_players:
                self.player_dict[id].move()

    def update_player(self, player_data):
        id, keys = player_data
        self.player_dict[id].update(keys)

    def prepare_send_object(self):
        # we don't want to send the whole player object on each network broadcast
        # so we create a temporary dictionary that the client can use to render the scene
        data_dict = {}
        for id in self.player_dict:
            if self.player_dict[id].gcd > 0:
                self.player_dict[id].gcd -= GAME_TICK
                if self.player_dict[id].gcd < 0:
                    self.player_dict[id].gcd = 0
            gcd = self.player_dict[id].gcd
            pos = (self.player_dict[id].x, self.player_dict[id].y)
            dir = self.player_dict[id].dir
            char_design = self.player_dict[id].char_design
            if self.player_dict[id].design_update:
                char_design["update"] = True
                self.player_dict[id].design_update = False
            else:
                char_design["update"] = False
            data = [pos, dir]
            send_data = {"pos_data" : data, "char_design" : char_design, "gcd" : gcd}
            data_dict[id] = send_data
        self.send_object = data_dict