from random import randint
from tw_player import Player
from tw_player_ai import Player as AI

class GameEngine:
    def __init__(self):
        self.on_start()
        self.registered_players = []

    def on_start(self):
        # all this is setting up AI players
        players_dict = {}
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
        data_dict = {}
        
        for id in self.player_dict:
            pos = (self.player_dict[id].x, self.player_dict[id].y)
            dir = self.player_dict[id].dir
            data = [pos, dir]
            data_dict[id] = data
        return data_dict

    def get_my_image(self, my_id):
        my_image = self.player_dict[my_id].player_image
        my_pos = (self.player_dict[my_id].x, self.player_dict[my_id].y)
        my_dir = self.player_dict[my_id].dir
        return (my_image, my_pos, my_dir)

    def update_images(self, my_id):
        temp_list = []
        for id in self.player_dict:
            if id == my_id:
                pass
            else:
                self.player_dict[id].update()
                image = self.player_dict[id].player_image
                pos = (self.player_dict[id].x, self.player_dict[id].y)
                dir = self.player_dict[id].dir
                temp_list.append([image, pos, dir])
        return temp_list