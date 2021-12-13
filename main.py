import itertools
import sys, pygame, json
from enum import Enum, IntEnum
import numpy as np
from random import randrange
import time

class GameState(Enum):
    PLAYING = None
    SOLVED = None
    FAILED = None

class TileState(IntEnum):
    NONE = 0
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
    tiles = []
    sudoku = []
    sudokuId = 0

    def __init__(self, id):
        self.game = "Sudoku"

        if id == 13:
            self.sudokuId = 0
        else:
            self.sudokuId = id
        if (self.sudokuId <= 2):
            self.tiles = [[Tile() for x in range(4)] for y in range(4)]
        else:
            self.tiles = [[Tile() for x in range(9)] for y in range(9)]
        self.__addNumbers()

    def getTile(self, row, column):
        return self.tiles[row][column]

    def addState(self, sudoku, i, x):
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


    def __addNumbers(self):
        with open('games.json', 'r') as j:
            json_data = json.load(j)
            self.sudoku = json_data[self.sudokuId]["field"]

        for i in range(len(self.tiles)):
            for x in range(len(self.tiles)):
                self.addState(self.sudoku, i, x)


def writeNumber(i, x):
    font = pygame.font.SysFont('times new roman', int(TILE_SIZE))
    stav = field.getTile(i, x).getTileState()
    text = font.render('{}'.format(stav), True, (0, 0, 0))
    return text

def writeText(text):
    font = pygame.font.SysFont('times new roman', 40)
    text = font.render('{}'.format(text), True, (255, 255, 255))
    return text

def setNewMap():
    global field 
    field = Field(field.sudokuId + 1)

def drawMap():
    posX = 0
    posY = 0

    for i in range(len(field.sudoku)):
        for x in range(len(field.sudoku)):
            if field.getTile(i, x).getTileState() != TileState.NONE:
                pygame.draw.rect(screen, (200, 200, 100), [x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                screen.blit(writeNumber(i,x), [posY + 10, posX])

            else:
                pygame.draw.rect(screen, (200, 200, 200), [x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE])
            posY += TILE_SIZE
        posY = 0
        posX += TILE_SIZE

    pygame.draw.rect(screen, (200, 100, 100), newFieldButtonRect)
    pygame.draw.rect(screen, (200, 100, 100), solveDFSRect)
    pygame.draw.rect(screen, (200, 100, 100), solveForwardRect)
    pygame.draw.rect(screen, (200, 100, 100), solveBacktrackRect)
    
    screen.blit(writeText('Nové pole'), [12*TILE_SIZE, 2*TILE_SIZE])
    screen.blit(writeText('DFS'), [12.6*TILE_SIZE, 4.1*TILE_SIZE])
    screen.blit(writeText('Forward'), [12.4*TILE_SIZE, 5.6*TILE_SIZE])
    screen.blit(writeText('Back'), [13*TILE_SIZE, 7.1*TILE_SIZE])

#PYGAME INIT AND SETTINGS
field = Field(0)
run = True

pygame.init()
WHITE = (255, 255, 255)
TILE_SIZE = (450 / 9)
size = width, height = 900, 450

screen = pygame.display.set_mode(size)
pygame.display.set_caption("SUDOKU")
screen.fill(WHITE)

newFieldButtonRect = pygame.Rect(11.6*TILE_SIZE, 1.9*TILE_SIZE, 4.2*TILE_SIZE, TILE_SIZE)
solveDFSRect = pygame.Rect(12.2*TILE_SIZE, 4*TILE_SIZE, 2.5*TILE_SIZE, TILE_SIZE)
solveForwardRect = pygame.Rect(12.2*TILE_SIZE, 5.5*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE)
solveBacktrackRect = pygame.Rect(12.2*TILE_SIZE, 7*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE)

#BACKTRACKING 
def isSafe(board, row, column, number):
    #kontrola ci najdem rovnake cislo v rovnakom riadku
    for x in range(len(field.sudoku)):
        if(board.getTile(row,x).getTileState() == number):
            return False

    #kontrola ci najdem rovnake cislo v rovnakom stlpci, vrati false ak niekde take cislo nasiel
    for x in range(len(field.sudoku)):
        if(board.getTile(x,column).getTileState() == number):
            return False

    #kontrola ci neni to iste cislo v stvorci 3x3
    stvorec = 2
    if (len(field.sudoku) > 4):
        stvorec = 3
    startRow = row - row % stvorec
    startColumn = column - column % stvorec

    for i in range(stvorec):
        for x in range(stvorec):
            if(board.getTile(i + startRow,x + startColumn).getTileState() == number):
                return False

    return True

def solveBacktrack(board, row, column):
    endRow = 3
    endColumn = 4
    if (len(field.sudoku) > 4):
        endRow = 8
        endColumn = 9

    # pre vyhnutie zlemu backtrackingu
    if (row == endRow and column == endColumn):
        return True

    #prejdenie na dalsi riadok ked dosiahnem posledny stlpec
    if (column == endColumn):
        column = 0
        row += 1

    #prechod na dalsie cislo ak tam uz je nejake zvolene
    if(board.getTile(row,column).getTileState() > 0):
        return solveBacktrack(board, row, column+1)

    for number in range(1, endColumn + 1, 1):
        if(isSafe(board, row, column, number)):
            board.getTile(row,column).setTileState(number)

            #skusanie dalsej moznosti
            if(solveBacktrack(board, row, column + 1)):
                return True
        #ak take cislo nemoze byt tak tam ide 0
        board.getTile(row,column).setTileState(0)

    return False


# DFS 
def isSolved():
    for i in range(len(field.sudoku)):
        for s in range(len(field.sudoku)):
            if field.sudoku[i].count(s + 1) > 1:
                return False
    
    for i in range(len(field.sudoku)):
        elements = set()

        for s in range(len(field.sudoku)):
            if field.sudoku[s][i] not in elements:
                elements.add(field.sudoku[s][i])
            else: return False

    return True

def getNumbers():
    pocet = 0
    zoznam = []
    for i in range(len(field.sudoku)):
        row = []
        cislo = 1
        for x in range(len(field.sudoku)):
            if(field.getTile(i, x).getTileState() == TileState.NONE):
                for y in range(len(field.sudoku)):
                    row.append(cislo)
                    cislo += 1
                pocet += 1
                zoznam.append(row)
            cislo = 1
            row = []

    return zoznam

def combineNumbers():
    for list in itertools.product(*getNumbers()):
        pozicia = 0
        for i in range(len(field.sudoku)):
            for x in range(len(field.sudoku)):
                if(field.getTile(i, x).getTileState() == TileState.NONE):
                    field.sudoku[i][x] = list[pozicia]
                    pozicia += 1

        if(isSolved()): 
            for i in range(len(field.sudoku)):
                for x in range(len(field.sudoku)):
                    field.addState(field.sudoku, i, x)

#FORWARD CHECKING
def isSafeForwardCheck(board, row, column, number):
    for x in range(len(field.sudoku)):
        if (board[row][x] == number):
            return False

    for x in range(len(field.sudoku)):
        if (board[x][column] == number):
            return False

    # kontrola ci neni to iste cislo v stvorci 3x3
    stvorec = 2
    if (len(field.sudoku) > 4):
        stvorec = 3
    startRow = row - row % stvorec
    startColumn = column - column % stvorec

    for i in range(stvorec):
        for x in range(stvorec):
            if (board[i + startRow][x + startColumn] == number):
                return False

    getOptions(board)
    return True


def getPossibleNumbers(row, column):
    zoznam = list(range(len(field.sudoku)))

    #zoznam = [1,2,3,4,5,6,7,8,9]

    for x in range(len(field.sudoku)):
        if(field.sudoku[row][x] in zoznam):
            zoznam.remove(field.sudoku[row][x])

    for x in range(len(field.sudoku)):
        if (field.sudoku[x][column] in zoznam):
            zoznam.remove(field.sudoku[x][column])
    return zoznam

def getOptions(board):
    zoznam = []
    for i in range(len(field.sudoku)):
        for x in range(len(field.sudoku)):
            if(board[i][x] == 0):
                zoznam.append(getPossibleNumbers(i, x))
    for i in range(len(zoznam)):
        if(len(zoznam[i]) == 0):
            return False
    return True

def isSafeOBJ(board, row, column, number):
    for x in range(len(field.sudoku)):
        if(board[row][x] == number):
            return False

    for x in range(len(field.sudoku)):
        if(board[x][column] == number):
            return False

    # kontrola ci neni to iste cislo v stvorci 3x3
    stvorec = 2
    if (len(field.sudoku) > 4):
        stvorec = 3
    startRow = row - row % stvorec
    startColumn = column - column % stvorec

    for i in range(stvorec):
        for x in range(stvorec):
            if(board[i + startRow][x + startColumn] == number):
                return False

    return True

def solve(board, row, column):
    endRow = 3
    endColumn = 4
    if (len(field.sudoku) > 4):
        endRow = 8
        endColumn = 9


    if (row == endRow and column == endColumn):
        return True

    if (column == endColumn):
        column = 0
        row += 1

    if(board[row][column] > 0):
        return solve(board, row, column+1)

    for number in range(1, endColumn + 1, 1):
        if(isSafeOBJ(board, row, column, number)):
            board[row][column] = number

            if(solve(board, row, column + 1)):
                return True
        board[row][column] = 0

    return False


def solveForwardChecking(board, row, column):
    endRow = 3
    endColumn = 4
    if (len(field.sudoku) > 4):
        endRow = 8
        endColumn = 9

    # pre vyhnutie zlemu backtrackingu
    if (row == endRow and column == endColumn):
        return True

    # prejdenie na dalsi riadok ked dosiahnem posledny stlpec
    if (column == endColumn):
        column = 0
        row += 1

    if(board[row][column] > 0):
        return solve(board, row, column+1)

    for number in range(1, endColumn + 1, 1):
        if(isSafeForwardCheck(board, row, column, number)):
            board[row][column] = number

            if(solveForwardChecking(board, row, column + 1)):
                return True
        board[row][column] = 0
    return False


# GAME PLAYING
while (run):
    pygame.time.delay(100)

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if newFieldButtonRect.collidepoint(pos):
                screen.fill(WHITE)
                setNewMap()
            if solveDFSRect.collidepoint(pos):
                tic = time.perf_counter()
                combineNumbers()
                toc = time.perf_counter()
                print(f"Downloaded the tutorial in {toc - tic:0.8f} seconds")
            if solveForwardRect.collidepoint(pos):
                tic = time.perf_counter()
                solveForwardChecking(field.sudoku, 0, 0)
                toc = time.perf_counter()
                print(f"Downloaded the tutorial in {toc - tic:0.8f} seconds")
                for i in range(len(field.sudoku)):
                    for x in range(len(field.sudoku)):
                        field.addState(field.sudoku, i, x)

            if solveBacktrackRect.collidepoint(pos):
                tic = time.perf_counter()
                solveBacktrack(field, 0, 0)
                toc = time.perf_counter()
                print(f"Downloaded the tutorial in {toc - tic:0.8f} seconds")
    drawMap()
    pygame.display.update()
