import math
import random
import time

import pygame
from color import *
from cell import Cell
from cell import Creature
from cell import Directions

SICK_PERCENT_PARAMETER = 0.5
FAST_PERCENT_PARAMETER = 0.2
NUM_GENERATIONS = 10
HIGH_INFECTION_PROB = 0.75
LOW_INFECTION_PROB = 0.25


class Grid:
    def __init__(self, rows, width, num_creatures, sick_percent, faster_percent, num_generations,
                 low_infection_prob, high_infection_prob):
        self.rows = self.cols = rows
        self.width = width
        self.cells = self.__make_cells()
        self.creatures = self.__make_creatures(num_creatures)
        self.sick_percent = sick_percent
        self.faster_percent = faster_percent
        self.num_generations = num_generations
        self.low_infection_prob = low_infection_prob
        self.high_infection_prob = high_infection_prob
        self.num_creatures = num_creatures

    def get_cell(self, row, col) -> Cell:
        return self.cells[col][row]  # care for index -> matrix is col major

    def draw(self, surface):
        surface.fill(WHITE)
        # draw all cells
        for row in self.cells:
            for cell in row:
                cell.draw(surface)

        # draw lines separating cells
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(surface, GREY, (0, i * gap), (self.width, i * gap))
        for j in range(self.cols):
            pygame.draw.line(surface, GREY, (j * gap, 0), (j * gap, self.width))

        pygame.display.update()

    def __make_cells(self):
        cell_width = self.width // self.rows
        return [[Cell(i, j, cell_width) for j in range(self.cols)] for i in range(self.rows)]

    def __wraparound(self, row, col):
        if row > (self.rows - 1):
            row -= self.rows
        elif row < 0:
            row += self.rows
        if col > (self.cols - 1):
            col -= self.cols
        elif col < 0:
            col += self.cols
        return row, col

    def __handle_collisions(self, moves):
        taken_positions = set([])
        for creature, (row, col) in moves.items():
            if (row, col) not in taken_positions:
                taken_positions.add((row, col))
            else:
                i = 0
                while True:  # keep picking new positions until no collision detected
                    new_row, new_col = self.__wraparound(*(creature.pick_move()))
                    if (new_row, new_col) not in taken_positions:
                        taken_positions.add((new_row, new_col))
                        moves[creature] = (new_row, new_col)
                        break
                    i += 1
                    if i == 5:
                        taken_positions.add((creature.row, creature.col))
                        moves[creature] = (creature.row, creature.col)
                        break

    def update(self):
        # map creature to it's picked move
        moves = {}
        for creature in self.creatures:
            movement_probability = random.random()
            # TODO if num_creatures is fewer than some T, then go to high infection prob
            if self.num_creatures <= 150*150:
                if movement_probability < HIGH_INFECTION_PROB:
                    moves[creature] = self.__wraparound(*(creature.pick_move()))
                else:
                    moves[creature] = (creature.row, creature.col)
            # TODO if num_creatures is bigger than some T, then go to low infection prob
            else:
                if movement_probability < LOW_INFECTION_PROB:
                    moves[creature] = self.__wraparound(*(creature.pick_move()))
                else:
                    moves[creature] = (creature.row, creature.col)
        # Directions.get_all_directions()
        # check no collision
        self.__handle_collisions(moves)
        # make moves
        for creature, (row, col) in moves.items():
            creature.make_move(row, col)

        # update cells to be white/black
        self.__update_cells()

    def __move_creatures(self):
        # make move - WRAP AROUND logic
        pass

    def __update_cells(self):
        """ update each cell in grid according to some logic """
        # make all cells free
        for row in range(self.rows):
            for col in range(self.cols):
                self.get_cell(row, col).set_free()
        # make cells where a creature is standing taken
        k = 0
        for i in range(int(len(self.creatures)*self.sick_percent)):
            row, col = self.creatures[k].get_pos()
            cell = self.get_cell(row, col)
            cell.set_sick_creature()
            k += 1
        for w in range(int(len(self.creatures)*self.faster_percent)):
            row, col = self.creatures[k].get_pos()
            cell = self.get_cell(row, col)
            cell.set_fast_creature()
            k += 1
        for j in range(int(len(self.creatures) * (1 - self.sick_percent - self.faster_percent))):
            row, col = self.creatures[k].get_pos()
            cell = self.get_cell(row, col)
            cell.set_taken_creature()
            k += 1

    def get_neighbor(self, cell: Cell) -> list[Cell]:
        row, col = cell.row, cell.col
        pass

    def __make_creatures(self, num_creatures):
        # pick positions for creatures
        positions = [(i, j) for j in range(self.cols) for i in range(self.rows)]
        random.shuffle(positions)
        creatures_positions = [positions.pop() for _ in range(num_creatures)]  # pick random pos w/o repeating
        creatures = [Creature(row, col) for row, col in creatures_positions]
        # set creatures in a cell
        for creature in creatures:
            row, col = creature.get_pos()
            cell = self.get_cell(row, col)
            cell.set_sick_creature()
        return creatures

if __name__ == '__main__':
    # setup
    dimension = 600
    ROWS = 200
    surface = pygame.display.set_mode((dimension, dimension))
    pygame.display.set_caption("Corona Infection Simulator")

    # cell environment setup
    grid = Grid(ROWS, dimension, 100*100, SICK_PERCENT_PARAMETER, FAST_PERCENT_PARAMETER,
                NUM_GENERATIONS, LOW_INFECTION_PROB, HIGH_INFECTION_PROB)
    game_running = True
    while game_running:
        grid.draw(surface)
        grid.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
    pygame.quit()

