import pygame
from random import choice
import random

find_index = lambda x, y: x + y * cols
a = int(input('\nВведите размер лабиринта: '))
print('Нумерация строк, столбов с 1 до', a)
start_x = int(input('Номер строки старта: '))-1
start_y = int(input('Номер столбца старта: '))-1

finish_y = int(input('Номер строки финиша: '))-1
finish_x = int(input('Номер столбца финиша: '))-1

        

RES = WIDTH, HEIGHT = 800, 800 #размер окна
TILE = WIDTH//int(a) #ширина ячейки в пикселях
cols, rows = WIDTH // TILE, HEIGHT // TILE #кол-во ячеек по гор-ли и верт-ли

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.sec_visited = False

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('grey'), (x + 2, y + 2, TILE - 2, TILE - 2))
        if self.x == 0 and self.y == 0:
            pygame.draw.rect(sc, pygame.Color('black'), (x + 2, y + 2, TILE - 2, TILE - 2))
    
    def draw_start(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('purple'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('white'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('white'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('white'), (x + TILE, y + TILE), (x , y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('white'), (x, y + TILE), (x, y), 2)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

    def check_walls(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.sec_visited and not self.walls['top']:
            neighbors.append(top)
        if right and not right.sec_visited and not self.walls['right']:
            neighbors.append(right)
        if bottom and not bottom.sec_visited and not self.walls['bottom']:
            neighbors.append(bottom)
        if left and not left.sec_visited and not self.walls['left']:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

#randnumb = random.randint(0,len(grid_cells))

current_cell = grid_cells[random.randint(0,len(grid_cells))]#0

stack = []
copy_cell = current_cell

way = []
way_sec = []
flag = False
flag_sec = False
start = grid_cells[find_index(start_x, start_y)]
finish = grid_cells[find_index(finish_x, finish_y)]
current_cell_sec = start
next_cell_sec = current_cell_sec

while True:
    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw() for cell in grid_cells] # отрисовка клеток поля
    current_cell.visited = True
    current_cell.draw_current_cell()
    
    #if flag:
        #start.draw_start()
        #finish.draw_start()
    if flag_sec:
        [cell_sec.draw_start() for cell_sec in way_sec]
        

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
 
    ########################

    if current_cell == copy_cell and flag==False:
        current_cell.sec_visited = True
        #current_cell_sec.draw_current_cell()

        next_cell_sec = current_cell_sec.check_walls()
        if next_cell_sec:
            next_cell_sec.sec_visited = True
            way.append(current_cell_sec)
            current_cell_sec = next_cell_sec
        elif way:
            current_cell_sec = way.pop()

        if current_cell_sec == finish:
            way.append(current_cell_sec)
            flag = True   

    if flag:

        if len(way) != 0:
            g = way[0]
            #g.draw_start()
            way_sec.append(g)
            way.pop(0)
            flag_sec = True
     
    pygame.display.flip()
    clock.tick(60)
