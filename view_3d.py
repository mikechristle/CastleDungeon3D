# ---------------------------------------------------------------------------
# Castle Dungeon 3D
# Mike Christle 2023
# ---------------------------------------------------------------------------

import state as st
import pygame as pg

from math import sin, cos, pi, floor
from paint import VIEW_WIDTH, VIEW_HEIGHT, view_image

FOV = 0.7
ANGLE_FACTOR = pi / 4.0
HALF_PI = pi / 2.0
MAX_DIST = 3.25

wall0_img = pg.image.load('Images/brick_wall0.png')
wall1_img = pg.image.load('Images/brick_wall1.png')
door0_img = pg.image.load('Images/door_wall0.png')
door1_img = pg.image.load('Images/door_wall1.png')
textures = [None, None, wall0_img, wall1_img, door0_img, door1_img]

TEX_WIDTH = 128
TEX_HEIGHT = 128

VIEW_HEIGHT_HALF = VIEW_HEIGHT // 2
MAX_WALL_HEIGHT = int(VIEW_HEIGHT / MAX_DIST) // 2
MAX_START = VIEW_HEIGHT_HALF - MAX_WALL_HEIGHT
MAX_STOP = VIEW_HEIGHT_HALF + MAX_WALL_HEIGHT

BLACK = '#000000'
FLOOR_COLOR = '#472500'
CEILING_COLOR = '#404040'
FLOOR = 0, VIEW_HEIGHT_HALF, VIEW_WIDTH, VIEW_HEIGHT_HALF
CEILING = 0, 0, VIEW_WIDTH, VIEW_HEIGHT_HALF


# ---------------------------------------------------------------------------
def make_3d_view():
    """Construct a 3D view."""

    # Draw floor and ceiling
    view_image.fill(CEILING_COLOR, CEILING)
    view_image.fill(FLOOR_COLOR, FLOOR)

    # Convert direction angle to radians
    angle = st.angle * ANGLE_FACTOR

    # Get direction vector
    dir_x = cos(angle)
    dir_y = -sin(angle)

    # Get view plane vector
    angle -= HALF_PI
    plane_x = cos(angle) * FOV
    plane_y = -sin(angle) * FOV

    # Set position to middle of current cell
    pos_x = st.pos_x + 0.5
    pos_y = st.pos_y + 0.5

    # For each vertical line in image
    for x in range(VIEW_WIDTH):

        # Get the current ray vector
        camera_x = (2.0 * x / VIEW_WIDTH) - 1.0
        ray_x = dir_x + plane_x * camera_x
        ray_y = dir_y + plane_y * camera_x

        delta_x = 1e30 if ray_x == 0.0 else abs(1.0 / ray_x)
        delta_y = 1e30 if ray_y == 0.0 else abs(1.0 / ray_y)

        map_x = int(st.pos_x)
        map_y = int(st.pos_y)

        if ray_x < 0:
            step_x = -1
            side_x = (pos_x - map_x) * delta_x
        else:
            step_x = 1
            side_x = (map_x + 1.0 - pos_x) * delta_x

        if ray_y < 0:
            step_y = -1
            side_y = (pos_y - map_y) * delta_y
        else:
            step_y = 1
            side_y = (map_y + 1.0 - pos_y) * delta_y

        while True:
            if side_x < side_y:
                side_x += delta_x
                map_x += step_x
                side = 0
            else:
                side_y += delta_y
                map_y += step_y
                side = 1

            # Check if ray has hit a wall
            wall = st.grid[map_y][map_x]
            if wall > 0: break

        if side == 0:
            wall_dist = side_x - delta_x
            wall_x = pos_y + (wall_dist * ray_y)
        else:
            wall_dist = side_y - delta_y
            wall_x = pos_x + (wall_dist * ray_x)
        wall_x -= floor(wall_x)

        if wall_dist > MAX_DIST:
            pg.draw.line(view_image, BLACK, (x, MAX_START), (x, MAX_STOP))
            continue

        # x coordinate on the texture
        tex_x = int(wall_x * TEX_WIDTH)
        if side == 0 and ray_x > 0:
            tex_x = TEX_WIDTH - tex_x - 1
        if side == 1 and ray_y < 0:
            tex_x = TEX_WIDTH - tex_x - 1

        # Calculate lowest and highest pixel to fill
        # in current stripe
        wall_height = int(VIEW_HEIGHT / wall_dist)
        draw_start = -wall_height // 2 + VIEW_HEIGHT // 2

        if abs(dir_y) > abs(dir_x):
            side ^= 1

        texture = textures[wall + side]
        line = texture.subsurface((tex_x, 0, 1, TEX_HEIGHT))
        line = pg.transform.scale(line, (1, wall_height))
        view_image.blit(line, (x, draw_start))
