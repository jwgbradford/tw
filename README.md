TinyWorld is an MMORPG (Miniature Multiplayer Online Role Playing Game)

The basic architecture is (will be):
game_engine <-> server <-> client -> renderer

We'll start with the renderer, then add some basic control, then the game engine, then split them into a client <-> server model. However, as that's our end-goal it will direct the design of the renderer and engine. For that reason we'll code them as separate files even when still in single-player, local-only mode.