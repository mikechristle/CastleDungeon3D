# ---------------------------------------------------------------------------
# Castle Dungeon 3D
# Construct a wall image
# Mike Christle 2023
# ---------------------------------------------------------------------------

from PIL import Image, ImageDraw

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
STEP_Y = IMAGE_HEIGHT // 8
STEP_X = IMAGE_WIDTH // 4

BG_COLOR = '#404040'
LN_COLOR = '#606060'

img0 = Image.new(mode="RGB", size=(IMAGE_WIDTH, IMAGE_HEIGHT), color=BG_COLOR)
img1 = ImageDraw.Draw(img0)

for y in range(8):
    y0 = y * STEP_Y

    line = ((0, y0), (IMAGE_WIDTH, y0))
    img1.line(line, fill=LN_COLOR, width=2)

    offset = STEP_X // 4
    if (y & 1) == 1:
        offset *= 3

    for x in range(4):
        x0 = (x * STEP_X) + offset
        line = ((x0, y0), (x0, y0 + STEP_Y))
        img1.line(line, fill=LN_COLOR, width=2)

img0.show()
img0.save('brick_wall.png')

