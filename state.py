# ---------------------------------------------------------------------------
# Castle Dungeon 3D
# Mike Christle 2023
# ---------------------------------------------------------------------------

from numpy import zeros
from cell import Cell

MAZE_SIZE = 8
MAZE_SIZE_MAX = MAZE_SIZE - 1

maze = [[Cell(x, y) for x in range(MAZE_SIZE)] for y in range(MAZE_SIZE)]

GRID_CELL = 2
GRID_SIZE = (MAZE_SIZE * GRID_CELL) + 1
GRID_SIZE_MAX = GRID_SIZE - 1
grid = zeros((GRID_SIZE, GRID_SIZE), dtype = int)

game_active = False
pos_x = GRID_CELL // 2
pos_y = GRID_CELL // 2
angle = 0
run_time = 0
sword_count = 0
coin_count = 0
rope_count = 0
monster_count = 0
pit_count = 0
slap_count = 0
message = ''
monsters = []

EMPTY = 0
WALL = 2
DOOR = 4

PIT = -1
MONSTER = -2
SWORD = -3
ROPE = -4
COIN = -5
