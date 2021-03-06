# SETUP
# install necessary packages
import subprocess
import sys
import pkg_resources
required = {'matplotlib', 'pygame'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

# START OF CODE
import random

import pygame
from color import *
from cell import Cell
from cell import Creature
from cell import Directions
import matplotlib.pyplot as plt

NUM_CREATURES = 1750
SICK_PERCENT_PARAMETER = 0.04
FAST_PERCENT_PARAMETER = 0.4
HIGH_INFECTION_PROB = 0.9
LOW_INFECTION_PROB = 0.1
T = 0.2
X = 15

class Grid:
    def __init__(self, rows, width, num_creatures, sick_percent, faster_percent,
                 low_infection_prob, high_infection_prob, T, X):
        self.rows = self.cols = rows
        self.width = width
        self.cells = self.__make_cells()
        self.creatures = self.__make_creatures(num_creatures, sick_percent, faster_percent)
        self.low_infection_prob = low_infection_prob
        self.high_infection_prob = high_infection_prob
        self.T = T
        self.X = X
        self.infection_calender = self.__make_infection_calender()

    def get_cell(self, row, col) -> Cell:
        return self.cells[row][col]

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

    def get_sickness_percent(self):
        count = 0
        for c in self.creatures:
            if c.is_sick():
                count += 1
        return count / len(self.creatures)

    def update(self):
        self.__move_creatures()
        self.__handle_infection()
        self.__update_calender()

    def __handle_infection(self):
        # infection
        sickness_percent = self.get_sickness_percent()
        for creature in self.creatures:
            if creature.is_sick():
                for neighbor in self.get_neighbors(creature):
                    if not neighbor.is_sick():  # sick creature can't be infected
                        p = random.random()
                        if sickness_percent > self.T:  # high % sickness -> hard to get infected
                            if p >= self.high_infection_prob:
                                neighbor.set_sick(True)
                                self.infection_calender[neighbor] = 0  # add him to calender
                        else:  # low % sickness -> easy to get infected
                            if p >= self.low_infection_prob:
                                neighbor.set_sick(True)
                                self.infection_calender[neighbor] = 0

    def __move_creatures(self):
        # each creature picks a move, set old cell as free and new cell as taken by creature
        for creature in self.creatures:
            possible_moves = self.get_possible_moves(creature)
            picked_move = creature.pick_move(possible_moves)
            self.get_cell(*(creature.get_pos())).set_free()
            creature.make_move(*picked_move)
            self.get_cell(*(creature.get_pos())).set_creature(creature)

    def __make_creatures(self, num_creatures, sick_percent, faster_percent):
        # generate all possible positions
        positions = [(i, j) for j in range(self.cols) for i in range(self.rows)]
        random.shuffle(positions)
        # pick random positions w/o repeating
        creatures_positions = [positions.pop() for _ in range(num_creatures)]
        # pick n_sick positions
        n_sick_creatures = int(num_creatures * sick_percent)
        random.shuffle(creatures_positions)
        sick_positions = set(creatures_positions[:n_sick_creatures])
        # pick n_fast positions, maybe overlapping with sick positions
        random.shuffle(creatures_positions)
        n_fast_creatures = int(num_creatures * faster_percent)
        fast_positions = set(creatures_positions[:n_fast_creatures])
        creatures_positions = set(creatures_positions)
        # divide into 4 groups
        # 1 - only sick
        only_sick_pos = sick_positions - fast_positions
        # 2 - sick and fast
        sick_fast_pos = sick_positions.intersection(fast_positions)
        # 3 - only fast
        only_fast_pos = fast_positions - sick_positions
        # 4 - normal
        normal_pos = creatures_positions - sick_positions - fast_positions
        # create list of different creatures
        creatures = [Creature(row, col, speed=Creature.BASE_SPEED, sick=False) for row, col in normal_pos] + \
                    [Creature(row, col, speed=Creature.FAST_SPEED, sick=False) for row, col in only_fast_pos] + \
                    [Creature(row, col, speed=Creature.BASE_SPEED, sick=True) for row, col in only_sick_pos] + \
                    [Creature(row, col, speed=Creature.FAST_SPEED, sick=True) for row, col in sick_fast_pos]
        # set creatures in cells
        for creature in creatures:
            row, col = creature.get_pos()
            cell = self.get_cell(row, col)
            cell.set_creature(creature)
        return creatures

    def get_possible_moves(self, creature: Creature):
        speed = creature.get_speed()
        row, col = creature.get_pos()
        future_positions = [self.__wraparound((dy * speed) + row, (dx * speed) + col)
                            for dy, dx in Directions.get_all_directions()]
        possible_moves = [(row, col) for row, col in future_positions if self.get_cell(row, col).is_free()]
        return possible_moves + [(row, col)]  # staying is always an option

    def get_neighbors(self, creature: Creature) -> list[Creature]:
        row, col = creature.get_pos()
        neighbors_pos = [self.__wraparound(dy + row, dx + col) for dy, dx in Directions.get_all_directions()]
        neighbors = []
        for row, col in neighbors_pos:
            neighbor_creature = self.get_cell(row, col).get_creature_or_none()
            if neighbor_creature:
                neighbors.append(neighbor_creature)
        return neighbors

    def __make_infection_calender(self):
        infection_calender = {}
        for creature in self.creatures:
            if creature.is_sick():
                infection_calender[creature] = 0
        return infection_calender

    def __update_calender(self):
        creatures_for_deletion = []  # need this cause dict can't changed size during iteration
        for creature, infected_days in self.infection_calender.items():
            self.infection_calender[creature] = infected_days + 1
            if self.infection_calender[creature] > self.X:
                creature.make_immune()
                creatures_for_deletion.append(creature)
        for creature in creatures_for_deletion:
            self.infection_calender.pop(creature)

def plot(X, Y):
    plt.plot(X, Y)
    plt.xlabel('Generation')
    plt.ylabel('Infected percent')
    plt.show()


if __name__ == '__main__':
    # setup
    dimension = 600
    ROWS = 200
    surface = pygame.display.set_mode((dimension, dimension))
    pygame.display.set_caption("Corona Infection Simulator")
    infected_percents = []
    generations = []
    gen = 0
    # cell environment setup
    grid = Grid(ROWS, dimension, NUM_CREATURES, SICK_PERCENT_PARAMETER, FAST_PERCENT_PARAMETER,
                LOW_INFECTION_PROB, HIGH_INFECTION_PROB, T, X)
    game_running = True
    while game_running:
        infected_percents.append(grid.get_sickness_percent())
        generations.append(gen)
        grid.draw(surface)
        grid.update()
        if grid.get_sickness_percent() == 0:
            game_running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        gen += 1
    pygame.quit()
    plot(X=generations, Y=infected_percents)

