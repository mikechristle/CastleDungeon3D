# ---------------------------------------------------------------------------
# Remove Background
# Mike Christle 2022
#
# Reads in a .bmp file, replaces all white pixels with transparency,
# then writes the image to a .png file.
# ---------------------------------------------------------------------------

from PIL import Image

FILE_NAME = r'Images\coin1.png'

with Image.open(FILE_NAME) as im:
    width, height = im.size
    img1 = Image.new('RGBA', (width, height))

    for y in range(height):
        for x in range(width):
            r, g, b, a = im.getpixel((x, y))
            if g > 220:
                img1.putpixel((x, y), (0, 0, 0, 0))
            else:
                img1.putpixel((x, y), (r, g, b, 255))

img1.save(FILE_NAME)
img1.show()

# for file in glob.glob(r'*.bmp'):
#     print(file)
#     file1 = file[:-3] + 'png'
#     img0 = Image.open(file)
#     img0.save(file1, 'PNG', transparency=BG_COLOR)
