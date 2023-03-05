# ---------------------------------------------------------------------------
# Castle Dungeon 3D
# Mike Christle 2023
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from time import time
from random import randrange

pg.mixer.init()
slap = pg.mixer.Sound('Sounds/Slap.wav')
ding = pg.mixer.Sound('Sounds/Ding.wav')
fall = pg.mixer.Sound('Sounds/Fall.wav')
fight = pg.mixer.Sound('Sounds/Fight.wav')
roar = pg.mixer.Sound('Sounds/Roar.wav')
tada = pg.mixer.Sound('Sounds/TaDa.wav')
whoop = pg.mixer.Sound('Sounds/Whoop.wav')
alarm = pg.mixer.Sound('Sounds/Alarm.wav')


# ---------------------------------------------------------------------------
def click(key):
    """Decode arrow keys and move the player."""

    # Right arrow rotates 45 degrees right
    if key == pg.K_RIGHT:
        st.angle = (st.angle - 1) & 7
        return

    # Left arrow rotates 45 degrees left
    if key == pg.K_LEFT:
        st.angle = (st.angle + 1) & 7
        return

    # Down key moves player backward
    x, y, a = st.pos_x, st.pos_y, st.angle
    if key == pg.K_DOWN:
        a ^= 4

    # Up key moves player forward
    # Ignore all other keys
    elif key != pg.K_UP:
        return

    # Decode the angle to get x y deltas
    match a:
        case 0:
            x += 1
        case 1:
            x += 1
            y -= 1
        case 2:
            y -= 1
        case 3:
            x -= 1
            y -= 1
        case 4:
            x -= 1
        case 5:
            x -= 1
            y += 1
        case 6:
            y += 1
        case 7:
            x += 1
            y += 1

    # If the new cell is not a wall, move to that cell
    cell_state = st.grid[y][x]
    if cell_state <= 0:
        st.pos_x, st.pos_y = x, y

    # Check the contents of the new cell
    match cell_state:

        # If an interior wall if slapped 5 times, it is removed
        case st.WALL:
            slap.play()
            if 0 < x < st.GRID_SIZE_MAX and 0 < y < st.GRID_SIZE_MAX:
                st.slap_count += 1
                if st.slap_count == 5:
                    st.grid[y][x] = 0
                else:
                    return

        # Finding the door ends the game
        case st.DOOR:
            st.game_active = False
            st.run_time = time() - st.run_time
            st.message = 'You found the exit door!'
            tada.play()

        # Walked onto a bottomless pit
        case st.PIT:

            # I the player has no rope,
            # he falls into the pit and the game ends
            if st.rope_count == 0:
                st.game_active = False
                st.run_time = time() - st.run_time
                st.message = 'You fell down a bottomless pit!'
                fall.play()

            # If player has rope he crosses the pit
            else:
                whoop.play()
                st.grid[y][x] = 0
                st.rope_count -= 1
                st.pit_count += 1

        # Player walks into a monster
        case st.MONSTER:

            # I the player has no sword,
            # he is eaten by the monster and the game ends
            if st.sword_count == 0:
                st.game_active = False
                st.run_time = time() - st.run_time
                st.message = 'You were eaten by a monster!'
                roar.play()

            # I player has a sword, he slays the monster
            else:
                fight.play()
                st.grid[y][x] = 0
                st.monsters.remove((x, y))
                st.sword_count -= 1
                st.monster_count += 1

        # Player found a rope
        case st.ROPE:
            st.rope_count += 1
            ding.play()
            st.grid[y][x] = 0

        # Player found a golc coin
        case st.COIN:
            st.coin_count += 1
            ding.play()
            st.grid[y][x] = 0

        # Player found a sword
        case st.SWORD:
            st.sword_count += 1
            ding.play()
            st.grid[y][x] = 0

    # Reset the slap count
    st.slap_count = 0


# ---------------------------------------------------------------------------
def check_alarm_timer():
    """Check the three minute bomb timer."""

    if st.game_active and (time() - st.run_time) >= 180.0:
        st.game_active = False
        st.message = 'The alarm sounded and you were captured.'
        st.run_time = 180.0
        alarm.play()


# ---------------------------------------------------------------------------
def move_monster():
    """Randomly move a monster."""

    # Abort if there are no monsters left
    n = len(st.monsters)
    if n == 0:
        return

    # Pick a random monster and remove it from the grid
    n = randrange(n)
    x, y = st.monsters.pop(n)
    st.grid[y][x] = 0

    # Pick a random direction to move
    match randrange(4):
        case 0 if x < st.GRID_SIZE_MAX and st.grid[y][x + 1] == 0:
            x += 1
        case 1 if y < st.GRID_SIZE_MAX and st.grid[y + 1][x] == 0:
            y += 1
        case 2 if x > 0 and st.grid[y][x - 1] == 0:
            x -= 1
        case 3 if y > 0 and st.grid[y - 1][x] == 0:
            y -= 1

    # Return the monster to the grid
    st.grid[y][x] = st.MONSTER
    st.monsters.append((x, y))

    # If the player is at the new location,
    # the player is eaten and the game ends
    if x == st.pos_x and y == st.pos_y:
        st.game_active = False
        st.run_time = time() - st.run_time
        st.message = 'You were eaten by a monster!'
        roar.play()
