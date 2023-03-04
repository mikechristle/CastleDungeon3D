# ---------------------------------------------------------------------------
# Castle Dungeon 3D
# A cell in the maze
# Mike Christle 2023
# ---------------------------------------------------------------------------

class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.top = False
        self.bot = False
        self.lft = False
        self.rit = False
        self.val = 0
        self.con = 0

    def clear(self):
        self.top = False
        self.bot = False
        self.lft = False
        self.rit = False
        self.con = 0
        self.val = 0

    def __repr__(self):
        return f'{self.x} {self.y} {self.val} {self.con}'
