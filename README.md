TinyWorld is an MMORPG (Miniature Multiplayer Online Role Playing Game)

The basic architecture is (will be):
game_engine <-> server <-> client -> renderer

You can switch between 'local' mode and 'network' mode by editing tw_client.py

Just multi-line comment out ( ''' ) or enable the lines between the mode comments.

If you're in netwok mode, you'll need to start tw_server.py and then run a tw_client.py

There are two 'ai' players wandering around for your entertainment, they don't do anything except wander aimlessly in a circle.

# To-Do
Lots!
1) background
2) objects to pick up / interact with
3) crafting / making stuff
4) walls / obstacles to go around

# Known bugs

# Solved bugs
1) pygame.K_LEFT works in local mode, but returns an 'index out of range' in network mode? If you print out pygame.K_LEFT it appears to be the same value in bode local / network mode, but it also appears to be wrong (should be 276 but is printing as 1073741904) - solved, the json encoding strips out the object wrapper from pygame.key.get_pressed() so have to use absolute key references