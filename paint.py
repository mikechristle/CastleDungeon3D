# ---------------------------------------------------------------------------
# Castle Dungeon 3D
# Mike Christle 2023
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

VIEW_HEIGHT = 675
VIEW_WIDTH = 1200
VIEW_HALF_HEIGHT = VIEW_HEIGHT // 2

# Initialize pygame and setup the window
pg.init()
pg.display.set_caption("Castle Dungeon 3D  V1.0")

screen = pg.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
view_image = pg.Surface((VIEW_WIDTH, VIEW_HEIGHT))

HEADER_FONT = pg.font.SysFont('Arial', 64)
INFO_FONT = pg.font.SysFont('Arial', 36)
STATUS_FONT = pg.font.SysFont('Arial', 48)

BLACK = 0, 0, 0
RED = 255, 0, 0

PIT1_RECT = 314, 580, 572, 230
PIT2_RECT = 427, 480, 346, 90
PIT3_RECT = 490, 440, 220, 30

img_coin = pg.image.load(r'Images\coin1.png')
img_sword = pg.image.load(r'Images\sword1.png')
img_monster = pg.image.load(r'Images\monster1.png')
img_rope = pg.image.load(r'Images\rope1.png')
img_small_rope = pg.image.load(r'Images\rope2.png')
img_small_sword = pg.image.load(r'Images\sword2.png')


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    if st.game_active:
        screen.blit(view_image, (0, 0))
        paint_objects()
        paint_status()
    else:
        paint_game_over()

    pg.display.update()


# ---------------------------------------------------------------------------
def paint_status():
    """
    Paint icons on the side of the screen to indicate
    the number of available swords and ropes.
    """

    # Paint rope icons on the left side of screen
    for y in range(st.rope_count):
        screen.blit(img_small_rope, (0, y * 40))

    # Paint sword icons on the right side of screen
    for y in range(st.sword_count):
        screen.blit(img_small_sword, (VIEW_WIDTH - 40, y * 40))


# ---------------------------------------------------------------------------
def paint_objects():
    """Paint objects that are visible to the player."""

    todo = get_objects()
    while len(todo) > 0:
        do = todo.pop()
        match do[0]:
            case st.PIT: pg.draw.ellipse(screen, BLACK, do[1])
            case st.COIN: paint_image(img_coin, do[1])
            case st.ROPE: paint_image(img_rope, do[1])
            case st.SWORD: paint_image(img_sword, do[1])
            case st.MONSTER: paint_image(img_monster, do[1])


# ---------------------------------------------------------------------------
def get_objects():
    """
    Build a list if objects that are visible to the player.
    The objects are ordered from nearest to farthest.
    """

    todo = []
    x, y = st.pos_x, st.pos_y
    dx = dy = 0
    match st.angle:
        case 0: dx += 1
        case 2: dy -= 1
        case 4: dx -= 1
        case 6: dy += 1
        case _: return todo

    # Check one step ahead
    x += dx
    y += dy

    # If cell is off the grid we are done
    if x < 0 or x >= st.GRID_SIZE or x < 0 or y >= st.GRID_SIZE: return todo

    # Check cell contents
    match st.grid[y][x]:
        case st.WALL | st.DOOR: return todo
        case st.PIT: todo.append((st.PIT, PIT1_RECT))
        case st.COIN: todo.append((st.COIN, (480, 420)))
        case st.ROPE: todo.append((st.ROPE, (600, 600)))
        case st.SWORD: todo.append((st.SWORD, (600, 331)))
        case st.MONSTER: todo.append((st.MONSTER, (600, 600)))

    # Check two step ahead
    x += dx
    y += dy

    # If cell is off the grid we are done
    if x < 0 or x >= st.GRID_SIZE or x < 0 or y >= st.GRID_SIZE: return todo

    # Check cell contents
    match st.grid[y][x]:
        case st.WALL | st.DOOR: return todo
        case st.PIT: todo.append((st.PIT, PIT2_RECT))
        case st.COIN: todo.append((st.COIN, (360, 280)))
        case st.ROPE: todo.append((st.ROPE, (400, 400)))
        case st.SWORD: todo.append((st.SWORD, (400, 220)))
        case st.MONSTER: todo.append((st.MONSTER, (400, 400)))

    # Check three step ahead
    x += dx
    y += dy

    # If cell is off the grid we are done
    if x < 0 or x >= st.GRID_SIZE or x < 0 or y >= st.GRID_SIZE: return todo

    # Check cell contents
    match st.grid[y][x]:
        case st.PIT: todo.append((st.PIT, PIT3_RECT))
        case st.COIN: todo.append((st.COIN, (180, 140)))
        case st.ROPE: todo.append((st.ROPE, (200, 200)))
        case st.SWORD: todo.append((st.SWORD, (200, 110)))
        case st.MONSTER: todo.append((st.MONSTER, (200, 200)))

    return todo


# ---------------------------------------------------------------------------
def paint_image(img, size):
    """Paint an image of the specified size in the center of the screen."""

    img = pg.transform.scale(img, size)
    rect = img.get_rect()
    rect.center = VIEW_WIDTH // 2, VIEW_HEIGHT // 2
    screen.blit(img, rect)


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        'You are a prisoner trapped in a dungeon!',
        'To escape you must find the green door.',
        'However, there are no lights, but you have a small',
        'lantern so you can see a little around yourself.',
        'Beware, there are monsters that will eat your bones.',
        'You can kill a monster if you have a sword.',
        'Watch your step, so you don\'t fall into a bottomless pit.',
        'You can cross a bottomless pit if you have a rope.',
        'Keep a lookout for gold coins. Each coin is worth $100.',
        'You have three minutes to escape before the alarm goes',
        'off and you are captured.',
        '',
        'Use arrow keys to move prisoner.',
        'Press the space bar to start a new game.',
    )

    screen.fill(BLACK)

    # Paint the game title
    text = HEADER_FONT.render("Castle Dungeon", True, RED)
    rect = text.get_rect()
    rect.center = (VIEW_WIDTH // 2, 40)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 100
    for line in intro:
        text = INFO_FONT.render(line, True, RED)
        rect = text.get_rect()
        rect.center = (VIEW_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 40

    pg.display.update()


# ---------------------------------------------------------------------------
def paint_game_over():
    """Paint the status screen at end of a game."""

    dollors = st.coin_count * 100
    screen.fill(BLACK)
    paint_text(st.message, 100)
    paint_text(f'Your time, {st.run_time:.0f} seconds.', 200)
    paint_text(f'Your found {st.coin_count} gold coins worth ${dollors}.', 260)
    paint_text(f'You slayed {st.monster_count} monsters.', 320)
    paint_text(f'You crossed over {st.pit_count} bottomless pits.', 380)
    paint_text('Press the space bar to start a new game.', 480)


# ---------------------------------------------------------------------------
def paint_text(text, y):
    """Paint a line of test, centered horizontally."""

    text = STATUS_FONT.render(text, True, RED)
    rect = text.get_rect()
    rect.center = (VIEW_WIDTH // 2, y)
    screen.blit(text, rect)
