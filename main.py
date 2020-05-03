from game import Game
from objects import Player, Tile
from resources import load_map
from sprite import GroupWithCamera, GroupSingleWithCamera

# Setup game
game = Game()
game_map = load_map("lvl1.txt")

# Create sprites
player = Player(20, 20)

# Add sprites to spritegroups
playersprite = GroupSingleWithCamera(player)
tilesprites = GroupWithCamera()
for y, row in enumerate(game_map):
    for x, tile in enumerate(row):
        if tile == "1":
            tilesprites.add(Tile("dirt", (x, y)))
        if tile == "2":
            tile_spr = Tile("grass", (x, y))
            tilesprites.add(tile_spr)

# Add spritegroups to game
game.add_spritegroups({"playersprite": playersprite, "tilesprites": tilesprites})

# Run game
game.initial_frame()
game.startloop()
