TinyWorld is an MMORPG (Miniature Multiplayer Online Role Playing Game)

The basic architecture is (will be):
game_engine <-> server <-> client -> renderer

Deleted 'local' mode as it was not needed. Network mode works.

There are two 'ai' players wandering around for your entertainment, they don't do anything except wander aimlessly in a circle.

The server code supports new players joining (up to 5 simultaneously), and currently players exiting. Cleans up connections when players leave. We don't trust the client, everything is done server-side.

# To-Do
Lots!
1) background
2) objects to pick up / interact with
3) crafting / making stuff
4) walls / obstacles to go around

# Known bugs

# Unknown bugs
1) At the moment we clean up when a player leaves by deleting their entry in two lists. What happens if our main loop is trying to read from those lists as they are being deleted? Not sure how if python provides a lock on dictionaries / lists to prevent this... should probably use queues for that, but then we'd have a known bug :D

# Solved bugs
1) pygame.K_LEFT works in local mode, but returns an 'index out of range' in network mode? If you print out pygame.K_LEFT it appears to be the same value in bode local / network mode, but it also appears to be wrong (should be 276 but is printing as 1073741904) - solved, the json encoding strips out the object wrapper from pygame.key.get_pressed() so have to use absolute key references