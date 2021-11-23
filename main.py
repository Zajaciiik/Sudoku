# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys, pygame
from enum import Enum
import numpy as np



#hra sa bude hrat kym je gamestate = Playing
class GameState(Enum):
    PLAYING = None
    SOLVED = None
    FAILED = None


#STAV dlazdice, predstavuje cislo ktore tam je
class TileState(Enum):
    NONE = 'X'
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

class Tile:

    def __init__(self, state = TileState.NONE):
        self.state = state

    def getTileState(self):
        return self.state

    def setTileState(self, state):
        self.state = state


class Field:
    tiles = [[Tile() for x in range(9)] for y in range(9)]

    #konstruktor
    def __init__(self):
        self.game = "Sudoku"
        self.__addNumbers()


    def getTile(self, row, column):
        return self.tiles[row][column]

    #prida stav do pola zo zoznamu sudoku
    def __addState(self, sudoku, i, x):
        #kontrolla cisla
        if (sudoku[i][x] == 0):
            self.getTile(i, x).setTileState(TileState.NONE)
        if (sudoku[i][x] == 1):
            self.getTile(i, x).setTileState(TileState.ONE)
        if (sudoku[i][x] == 2):
            self.getTile(i, x).setTileState(TileState.TWO)
        if (sudoku[i][x] == 3):
            self.getTile(i, x).setTileState(TileState.THREE)
        if (sudoku[i][x] == 4):
            self.getTile(i, x).setTileState(TileState.FOUR)
        if (sudoku[i][x] == 5):
            self.getTile(i, x).setTileState(TileState.FIVE)
        if (sudoku[i][x] == 6):
            self.getTile(i, x).setTileState(TileState.SIX)
        if (sudoku[i][x] == 7):
            self.getTile(i, x).setTileState(TileState.SEVEN)
        if (sudoku[i][x] == 8):
            self.getTile(i, x).setTileState(TileState.EIGHT)
        if (sudoku[i][x] == 9):
            self.getTile(i, x).setTileState(TileState.NINE)


    #pridanie cisla na zaciatok
    def __addNumbers(self):
        sudoku = [
            [8,0,0,9,3,0,0,0,2],
            [0,0,9,0,0,0,0,4,0],
            [7,0,2,1,0,0,9,6,0],
            [2,0,0,0,0,0,0,9,0],
            [0,6,0,0,0,0,0,7,0],
            [0,7,0,0,0,6,0,0,5],
            [0,2,7,0,0,8,4,0,6],
            [0,3,0,0,0,0,5,0,0],
            [5,0,0,0,6,2,0,0,8]
        ]

        for i in range(9):
            for x in range(9):
                self.__addState(sudoku, i, x)


field = Field()
print("GOOD LUCK")
print()

for i in range(len(field.tiles)):
    for x in range(len(field.tiles)):
        print("{}".format(field.getTile(i, x).getTileState().value), end=" ")
    print()




#HRA
pygame.init()
BLUE = (0, 0, 200)
size = width, height = 450, 450
TILE_SIZE = (450 / 9)


screen = pygame.display.set_mode(size)
pygame.display.set_caption("SUDOKU MAP 1")
screen.fill(BLUE)

#drawMap
def drawMap():
    font = pygame.font.SysFont('times new roman', int(TILE_SIZE))
    text = font.render('9', True, (0, 0, 0))

    for i in range(9):
         for x in range(9):
            #draw Map
            if field.getTile(i, x).getTileState() != TileState.NONE:
                pygame.draw.rect(screen, (200, 200, 100), [x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                screen.blit(text, [i, x])
            else:
                pygame.draw.rect(screen, (200, 200, 200), [x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE])

# gameState = GameState.PLAYING
run = True
while (run):
    pygame.time.delay(100)

    #aby som mohol vypnut bez erroru, co robi uzivatel
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()

    drawMap()
    pygame.display.update()





