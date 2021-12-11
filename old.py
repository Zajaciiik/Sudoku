# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys, pygame, json
from enum import Enum
from random import randrange


POCITADLO = 0

#hra sa bude hrat kym je gamestate = Playing
class GameState(Enum):
    PLAYING = None
    SOLVED = None
    FAILED = None


#STAV dlazdice, predstavuje cislo ktore tam je


field = [[]]

def initField(fieldId):
    with open('games.json', 'r') as j:
        json_data = json.load(j)
        return json_data[fieldId]["field"]

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

def solveBack(board, row, column, pocitadlo):
    # pre vyhnutie zlemu backtrackingu
    if (row == 8 and column == 9):
        return True

    #prejdenie na dalsi riadok ked dosiahnem posledny stlpec
    if (column == 9):
        column = 0
        row += 1

    #prechod na dalsie cislo ak tam uz je nejake zvolene

    if(board[row][column] > 0):
        return solveBack(board, row, column+1, pocitadlo)

    for number in range(1, 10, 1):
        if(isSafe(board, row, column, number)):
            #nahradenie 0 za zvolene cislo
            
            board[row][column] = number

            #skusanie dalsej moznosti
            if(solveBack(board, row, column + 1, pocitadlo)):
                return True

        #ak take cislo nemoze byt tak tam ide 0
        board[row][column] = 0

    return False

#tato fukncia zisti aky stav je dlazdica a vrati string cisla
def writeNumber(i, x):
    font = pygame.font.SysFont('times new roman', int(TILE_SIZE))
    stav = field[i][x]
    text = font.render('{}'.format(stav), True, (0, 0, 0))
    return text

def writeText(text):
    font = pygame.font.SysFont('times new roman', 40)
    text = font.render('{}'.format(text), True, (255, 255, 255))
    return text

#HRA
pygame.init()
WHITE = (255, 255, 255)
size = width, height = 900, 450
TILE_SIZE = (450 / 9)
field = initField(0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("SUDOKU")
screen.fill(WHITE)

newFieldButtonRect = pygame.Rect(11.6*TILE_SIZE, 1.9*TILE_SIZE, 4.2*TILE_SIZE, TILE_SIZE)
solveButtonRect = pygame.Rect(12.2*TILE_SIZE, 4*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE)

def setNewMap():
    global field 
    field = initField(randrange(10))

def solveMap():
    solveBack(field, 0, 0, 0)

#drawMap
def drawMap():
    posX = 0
    posY = 0

    for i in range(9):
        for x in range(9):
            #draw Map
            if field[i][x] != 0:
                pygame.draw.rect(screen, (200, 200, 100), [x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                screen.blit(writeNumber(i,x), [posY+10, posX])

            else:
                pygame.draw.rect(screen, (200, 200, 200), [x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE])
            posY += TILE_SIZE
        posY = 0
        posX += TILE_SIZE

    pygame.draw.rect(screen, (200, 100, 100), newFieldButtonRect)
    screen.blit(writeText('Nové pole'), [12*TILE_SIZE, 2*TILE_SIZE])

    pygame.draw.rect(screen, (200, 100, 100), solveButtonRect)
    screen.blit(writeText('Vyrieš'), [12.6*TILE_SIZE, 4.1*TILE_SIZE])

# gameState = GameState.PLAYING
run = True
while (run):
    ev = pygame.event.get()
    pygame.time.delay(100)

    #aby som mohol vypnut bez erroru, co robi uzivatel
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if newFieldButtonRect.collidepoint(pos):
                setNewMap()
            if solveButtonRect.collidepoint(pos):
                solveMap()
    drawMap()
    pygame.display.update()





