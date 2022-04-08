import random

from color import *
import pygame

class Cell:
    def __init__(self, row, col, cell_width):
        self.row = row
        self.col = col
        self.x = row * cell_width
        self.y = col * cell_width
        # self.color = random.choice([WHITE, BLACK])
        self.color = WHITE
        self.neighbors = []
        self.width = cell_width

    def get_pos(self):
        return self.row, self.col

    def is_free(self):
        return self.color == WHITE  # black means it has a creature on it

    def set_free(self):
        self.color = WHITE

    def is_creature(self):
        return self.color == RED  # black means it has a creature on it

    def is_sick(self):
        return self.color == BLACK  # black means it has a creature on it

    def is_fast(self):
        return self.color == PURPLE

    def set_taken_creature(self):
        self.color = RED

    def set_sick_creature(self):
        self.color = BLACK

    def set_fast_creature(self):
        self.color = GREEN

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    # def update_neighbors(self, grid):
    #     self.neighbors = []
    #     # Down neighbor
    #     if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():
    #         self.neighbors.append(grid[self.row + 1][self.col])
    #     # Up neighbor
    #     if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
    #         self.neighbors.append(grid[self.row - 1][self.col])
    #     # Right neighbor
    #     if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
    #         self.neighbors.append(grid[self.row][self.col + 1])
    #     # Left neighbor
    #     if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
    #         self.neighbors.append(grid[self.row][self.col - 1])


class Creature:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def pick_move(self):
        positions = []
        # stay
        positions.append((self.row, self.col))
        # ↑
        positions.append((self.row-1, self.col))
        # →
        positions.append((self.row, self.col+1))
        # ↓
        positions.append((self.row+1, self.col))
        # ←
        positions.append((self.row, self.col-1))
        # ↖
        positions.append((self.row-1, self.col-1))
        # ↗
        positions.append((self.row-1, self.col+1))
        # ↘
        positions.append((self.row+1, self.col+1))
        # ↙
        positions.append((self.row+1, self.col-1))
        return random.choice(positions)

    def pick_fast_move(self):
        positions = []
        # stay
        positions.append((self.row, self.col))
        # ↑
        positions.append((self.row-10, self.col))
        # →
        positions.append((self.row, self.col+10))
        # ↓
        positions.append((self.row+10, self.col))
        # ←
        positions.append((self.row, self.col-10))
        # ↖
        positions.append((self.row-10, self.col-10))
        # ↗
        positions.append((self.row-10, self.col+10))
        # ↘
        positions.append((self.row+10, self.col+10))
        # ↙
        positions.append((self.row+10, self.col-10))
        return random.choice(positions)

    def make_move(self, row, col):
        self.row = row
        self.col = col

    def get_pos(self):
        return self.row, self.col

class Directions:
    # stay
    STAY = (0, 0)
    # ↑
    UP = (-1, 0)
    # →
    RIGHT = (0, +1)
    # ↓
    DOWN = (+1, 0)
    # ←
    LEFT = (0, -1)
    # ↖
    UP_LEFT = (-1, -1)
    # ↗
    UP_RIGHT = (-1, +1)
    # ↘
    DOWN_RIGHT = (+1, +1)
    # ↙
    DOWN_LEFT = (+1, -1)

    @classmethod
    def get_all_directions(cls):
        return [Directions.UP, Directions.RIGHT, Directions.LEFT, Directions.DOWN,
                Directions.UP_LEFT, Directions.UP_RIGHT, Directions.DOWN_RIGHT, Directions.DOWN_LEFT]


