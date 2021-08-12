import pygame
from random import randint
from tw_objects import Player, NPC, Weapon
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
        self.player_dict = {}
        # setting up AI players
        ai_1 =  "p" + str(randint(0, 64000))
        ai_2 =  "p" + str(randint(0, 64000))
        self.player_dict[ai_1] = NPC(ai_1, (100,100), 0)
        self.player_dict[ai_2] = NPC(ai_2, (300,300), 0)

        self.items_dict = {}
        weapon = "i" + str(randint(64001, 127999))
        self.items_dict[weapon] = Weapon(weapon, (300, 100), 0)
        self.prepare_send_object()

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
        send_data = {}
        send_players = {}
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
            player_data = {"pos_data" : data, "char_design" : char_design, "gcd" : gcd}
            send_players[id] = player_data
        send_data["players"] = send_players
        send_items = {}
        for id in self.items_dict:
            pos = (self.items_dict[id].x, self.items_dict[id].y)
            dir = self.items_dict[id].dir
            obj_design = self.items_dict[id].obj_design
            object_data = {"pos_data" : data, "char_design" : obj_design}
            send_items[id] = object_data
        send_data["objects"] = send_items
        return send_data