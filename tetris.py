import pygame
from pygame.locals import *
from collections import namedtuple
import math
import random
from blocks import *
pygame.init()

timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
score_surf = font.render("Score: "+ str(score), True, (255,255,255), None)
SCREENSIZE = (1600, 900)
screen = pygame.display.set_mode(SCREENSIZE)
position = namedtuple("Position", ["x", "y"])
size = namedtuple("Size", ["width", "height"])
BLOCKSIZE = 50

lines = []
scr = 900
for i in range(17):
    lines.append(scr)
    scr -= BLOCKSIZE

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.pos = position(x, y)
        self.size = size(width, height)
        self.color = color
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect = self.image.get_rect(center=self.pos)

class Element():
    def __init__(self, pattern,color):
        self.blocks = pygame.sprite.Group()
        main_block_coords = pattern[0]
        self.moving = True
        self.main_block = Block(main_block_coords.x, main_block_coords.y, BLOCKSIZE, BLOCKSIZE, color)
        self.blocks.add(self.main_block)
        for block_coords in pattern:
            if block_coords == self.main_block.pos:
                continue
            block = Block(block_coords.x, block_coords.y, BLOCKSIZE, BLOCKSIZE, color)
            self.blocks.add(block)

    def rotate(self):
        for block in self.blocks:
            if block.pos == self.main_block.pos:
                continue
            if self.on_one_axis(block):
                if block.pos.x < self.main_block.pos.x:
                    self.rotate_block(block, 0) ########
                elif block.pos.x > self.main_block.pos.x:
                    self.rotate_block(block, 1)
                elif block.pos.y < self.main_block.pos.y:
                    self.rotate_block(block, 2)
                elif block.pos.y > self.main_block.pos.y:  ########
                    self.rotate_block(block, 3)
            else:
                pass

    def on_one_axis(self, block):
        if self.main_block.pos.x == block.pos.x or self.main_block.pos.y == block.pos.y:
            return True
        return False

    def rotate_block(self, block, side):
        if self.moving:
            d = abs(block.pos.x - self.main_block.pos.x) if block.pos.x - self.main_block.pos.x != 0 else abs(block.pos.y - self.main_block.pos.y)
            match side:
                case 0:
                    block.pos = position(self.main_block.pos.x, self.main_block.pos.y - d)
                case 1:
                    block.pos = position(self.main_block.pos.x, self.main_block.pos.y + d)
                case 2:
                    block.pos = position(self.main_block.pos.x + d, self.main_block.pos.y)
                case 3:
                    block.pos = position(self.main_block.pos.x - d, self.main_block.pos.y)
            self.blocks.update()

    def get_edge_blocks(self):
        max_x = 0
        min_x = 0
        for block in self.blocks:
            if max_x == 0 or block.pos.x > max_x:
                max_x = block.pos.x
            if min_x == 0 or block.pos.x < min_x:
                min_x = block.pos.x
        return min_x, max_x

    def move(self):
        if self.moving and t %2 != 0:
            min_x, max_x = self.get_edge_blocks()
            pygame.draw.line(screen, (255,255,255), (min_x, self.main_block.pos.y + BLOCKSIZE/2),(min_x, 900), 10)
            pygame.draw.line(screen, (255,255,255), (max_x, self.main_block.pos.y + BLOCKSIZE/2),(max_x, 900), 10)
            def check_other(bloc):
                for element in elements:
                    if element == self:
                        continue
                    for block in element.blocks:
                        if block.pos.y == bloc.pos.y + BLOCKSIZE and block.pos.x == bloc.pos.x:
                            return True
                return False

            for block in self.blocks:
                block.pos = position(block.pos.x, block.pos.y + BLOCKSIZE)
                if block.pos.y >= SCREENSIZE[1] - BLOCKSIZE:
                    self.moving = False
                if check_other(block):
                    self.moving = False
            self.blocks.update()

    def move_idk(self):
        if self.moving:
            keys = pygame.key.get_pressed()

            def check_block(more, number):
                if more:
                    for block in self.blocks:
                        if block.pos.x > number:
                            return False
                else:
                    for block in self.blocks:
                        if block.pos.x < number:
                            return False
                return True

            if check_block(False, 400):
                if keys[K_a]:
                    for block in self.blocks:
                        block.pos = position(block.pos.x - BLOCKSIZE, block.pos.y)

            if check_block(True, 1200):
                if keys[K_d]:
                    for block in self.blocks:
                        block.pos = position(block.pos.x + BLOCKSIZE, block.pos.y)

def draw_borders():
    pygame.draw.line(screen, (255,255,255), (350, 0), (350, SCREENSIZE[1]), 10)
    pygame.draw.line(screen, (255,255,255), (1250, 0), (1250, SCREENSIZE[1]), 10)

def check_new():
    for element in elements:
        if element.moving == True:
            return False
    return True

def dima(): # 19
    global score
    global score_surf
    for line in lines:
        total = 0
        for element in elements:
            for block in element.blocks:
                if block.pos.y == line:
                    total += 1
        if total >= 19:
            score += 1
            score_surf = font.render("Score: "+str(score), True, (255,255,255), None)
            clear_the_area(line)

def clear_the_area(line):
    for element in elements:
        for block in element.blocks:
            if block.pos.y == line:
                element.blocks.remove(block)
                block = None
                continue
            if block.pos.y < line:
                block.pos = position(block.pos.x, block.pos.y + BLOCKSIZE)
                block.update()
game_on = True
t = 0
elements = []
element = Element(blocks_pattern[random.randint(0, len(blocks_pattern)-1)], (255,255,255))
elements.append(element)

while game_on:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.KEYDOWN:
            for element in elements:
                if event.key == pygame.K_r:
                    element.rotate()
                element.move_idk()

    if check_new():
        element1 = Element(blocks_pattern[random.randint(0, len(blocks_pattern)-1)], (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        elements.append(element1)
        dima()

    screen.fill((0,0,0))
    draw_borders()
    screen.blit(score_surf, (1300, 50))
    for element in elements:
        element.move()
        element.blocks.draw(screen)
    
    timer.tick(10)
    t += 1
    pygame.display.flip()