# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys, pygame
from enum import Enum
import numpy as np

POCITADLO = 0

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


#Depth First Search algoritmus

#funkcia ktora zisti ci na toto miesto mozes jebnut cislo
def isSafe(board, row, column, number):

    #kontrola ci najdem rovnake cislo v rovnakom riadku
    for x in range(9):
        if(board[row][x] == number):
            return False

    #kontrola ci najdem rovnake cislo v rovnakom stlpci, vrati false ak niekde take cislo nasiel
    for x in range(9):
        if(board[x][column] == number):
            return False

    #kontrola ci neni to iste cislo v stvorci 3x3
    startRow = row - row % 3
    startColumn = column - column % 3
    for i in range(3):
        for x in range(3):
            if(board[i + startRow][x + startColumn] == number):
                return False

    #presli vsetky kontrolky
    return True

def solve(board, row, column, pocitadlo):


    # pre vyhnutie zlemu backtrackingu
    if (row == 8 and column == 9):
        return True

    #prejdenie na dalsi riadok ked dosiahnem posledny stlpec
    if (column == 9):
        column = 0
        row += 1

    #prechod na dalsie cislo ak tam uz je nejake zvolene
    if(board[row][column] > 0):
        return solve(board, row, column+1)

    for number in range(1, 10, 1):
        if(isSafe(board, row, column, number)):
            #nahradenie 0 za zvolene cislo
            board[row][column] = number

            #skusanie dalsej moznosti
            if(solve(board, row, column + 1)):
                return True
        #ak take cislo nemoze byt tak tam ide 0
        board[row][column] = 0


    return False






field = Field()
print("GOOD LUCK")
print()

for i in range(len(field.tiles)):
    for x in range(len(field.tiles)):
        print("{}".format(field.getTile(i, x).getTileState().value), end=" ")
    print()
# sudoku = [
#             [8,4,6,9,3,0,0,0,2],
#             [3,1,9,6,2,5,0,4,0],
#             [7,5,2,1,8,4,9,6,0],
#             [2,8,5,7,1,3,6,9,4],
#             [4,6,3,8,5,9,2,7,1],
#             [9,7,1,2,4,6,3,8,5],
#             [0,2,7,0,0,8,4,0,6],
#             [0,3,0,0,0,0,5,0,0],
#             [5,9,4,3,6,2,0,0,8]
#         ]
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
solve(sudoku, 0, 0)

print("Vyriesene: ")
for i in range(9):
    for x in range(9):
        print(sudoku[i][x], end=" ")
    print()


#tato fukncia zisti aky stav je dlazdica a vrati string cisla
def writeNumber(i, x):
    font = pygame.font.SysFont('times new roman', int(TILE_SIZE))
    stav = field.getTile(i, x).getTileState().value
    text = font.render('{}'.format(stav), True, (0, 0, 0))
    return text

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
    posX = 0
    posY = 0

    for i in range(9):
        for x in range(9):
            #draw Map
            if field.getTile(i, x).getTileState() != TileState.NONE:
                pygame.draw.rect(screen, (200, 200, 100), [x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                screen.blit(writeNumber(i,x), [posY, posX])


            else:
                pygame.draw.rect(screen, (200, 200, 200), [x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE])
            posY += TILE_SIZE
        posY = 0
        posX += TILE_SIZE

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





