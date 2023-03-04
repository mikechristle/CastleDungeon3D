# ---------------------------------------------------------------------------
# Castle Dungeon 3D
# Mike Christle 2023
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from random import randrange
from make_maze import make_maze
from paint import paint, paint_intro
from view_3d import make_3d_view
from game_logic import click, move_monster
from time import time


# ---------------------------------------------------------------------------
def main():
    """Main event loop."""

    # 1.0 Second timer event to move monsters
    pg.time.set_timer(pg.USEREVENT, 1000)

    paint_intro()
    while True:

        # Get all pygame events
        for event in pg.event.get():
            match [event.type, st.game_active]:

                # Exit if window is closed
                case [pg.QUIT, _]:
                    exit()

                # Space bar start a game
                case [pg.KEYDOWN, False]:
                    if event.key == pg.K_SPACE:
                        make_maze()
                        fill_grid()
                        make_3d_view()
                        paint()
                        st.run_time = time()

                # Arrow keys move the player
                case [pg.KEYDOWN, True]:
                    click(event.key)
                    make_3d_view()
                    paint()

                # One second timer to move monsters
                case [pg.USEREVENT, True]:
                    move_monster()
                    make_3d_view()
                    paint()


# ---------------------------------------------------------------------------
def fill_grid():
    """Copy walls from the maze to the view grid."""

    # Position the player in the corner of the maze
    st.game_active = True
    st.pos_x = st.GRID_CELL // 2
    st.pos_y = st.GRID_CELL // 2
    st.angle = 0
    st.sword_count = 0
    st.coin_count = 0
    st.rope_count = 0
    st.monster_count = 0
    st.pit_count = 0
    st.slap_count = 0

    # Clear all walls from previous game
    for y in range(st.GRID_SIZE):
        for x in range(st.GRID_SIZE):
            st.grid[y][x] = st.EMPTY

    # Fill in the internal walls of the maze
    for y in range(st.MAZE_SIZE):
        y0 = y * st.GRID_CELL
        for x in range(st.MAZE_SIZE):
            x0 = x * st.GRID_CELL
            cell = st.maze[y][x]
            if not cell.lft:
                for y1 in range(y0, y0 + st.GRID_CELL):
                    st.grid[y1][x0] = st.WALL
            if not cell.top:
                for x1 in range(x0, x0 + st.GRID_CELL):
                    st.grid[y0][x1] = st.WALL
            if cell.lft and cell.top:
                st.grid[y0][x0] = st.WALL

    # Fill in the border walls
    for x in range(st.GRID_SIZE):
        st.grid[0][x] = st.WALL
    for y in range(st.GRID_SIZE):
        st.grid[y][0] = st.WALL
    for x in range(st.GRID_SIZE):
        st.grid[st.GRID_SIZE_MAX][x] = st.WALL
    for y in range(st.GRID_SIZE):
        st.grid[y][st.GRID_SIZE_MAX] = st.WALL

    # Add a door
    while True:
        xy = randrange(st.GRID_SIZE)
        if st.grid[1][xy] == 0:
            st.grid[0][xy] = st.DOOR
            break
        if st.grid[st.GRID_SIZE - 2][xy] == 0:
            st.grid[st.GRID_SIZE - 1][xy] = st.DOOR
            break
        if st.grid[xy][1] == 0:
            st.grid[xy][0] = st.DOOR
            break
        if st.grid[xy][st.GRID_SIZE - 2] == 0:
            st.grid[xy][st.GRID_SIZE - 1] = st.DOOR
            break

    # Add Objects
    st.monsters.clear()
    add_object(st.COIN, 10)
    add_object(st.MONSTER, 4)
    add_object(st.SWORD, 4)
    add_object(st.PIT, 4)
    add_object(st.ROPE, 4)


# ---------------------------------------------------------------------------
def add_object(obj, count):
    """Add an object to a random location on the grid."""

    while count > 0:
        x = randrange(st.GRID_SIZE)
        y = randrange(st.GRID_SIZE)
        if st.grid[y][x] == 0:
            st.grid[y][x] = obj
            count -= 1

            # Save the location of monsters so they can move
            if obj == st.MONSTER:
                st.monsters.append((x, y))


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()

