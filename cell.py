import random

from color import *
import pygame

class Creature:
    BASE_COLOR = GREEN
    SICK_COLOR = RED
    BASE_SPEED = 1
    FAST_SPEED = 10

    def __init__(self, row: int, col: int, speed: int, sick: bool):
        self.row = row
        self.col = col
        self.speed = speed
        self.sick = sick
        self.movement_strategy = random.choice  # can have any type of picking strategy
        self.immune = False


    def pick_move(self, moves: list):
        return self.movement_strategy(moves)

    def make_move(self, row, col):
        self.row = row
        self.col = col

    def get_pos(self):
        return self.row, self.col

    def is_sick(self):
        return self.sick

    def set_sick(self, sick: bool):
        if not self.immune:
            self.sick = sick

    def get_sickness_state(self) -> tuple[int, int, int]:
        if self.sick:
            return Creature.SICK_COLOR
        else:
            return Creature.BASE_COLOR

    def get_speed(self):
        return self.speed

    def make_immune(self):
        self.immune = True
        self.sick = False

class Cell:
    BASE_COLOR = WHITE

    def __init__(self, row, col, cell_width):
        self.row = row
        self.col = col
        self.x = row * cell_width
        self.y = col * cell_width
        self.color = WHITE
        self.neighbors = []
        self.width = cell_width
        self.creature = None

    def set_creature(self, creature: Creature):
        self.creature = creature

    def get_creature_or_none(self):
        return self.creature

    def get_pos(self):
        return self.row, self.col

    def is_free(self) -> bool:
        return self.creature is None

    def set_free(self):
        self.creature = None

    def draw(self, surface):
        if self.creature:  # reflect creature's sickness color on cell
            pygame.draw.rect(surface, self.creature.get_sickness_state(), (self.x, self.y, self.width, self.width))
        else:
            pygame.draw.rect(surface, Cell.BASE_COLOR, (self.x, self.y, self.width, self.width))

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



class Directions:
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


