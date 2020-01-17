import pygame, sys, time
from pygame.locals import *
from random import *






#Color list

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
ORANGE = (255,152,0)
DEEP_ORANGE = (255,87,34)
BROWN = (121,85,72)
GREEN = (0,128,0)
LIGHT_GREEN = (139,195,74)
TEAL = (0,150,136)
BLUE = (33,150,136)
PURPLE = (156,39,176)
PINK = (234,30,99)
DEEP_PURPLE = (103,58,183)

colors = {
    0:BLACK,
    2:RED,
    4:GREEN,
    8:PURPLE,
    16:DEEP_PURPLE,
    32:DEEP_ORANGE,
    64:TEAL,
    128:LIGHT_GREEN,
    256:BROWN,
    512:ORANGE,
    1024:BLUE,
    2048:PINK
}

def getColors(i):
    return colors[i]


SIZE_BOARD = 4
TOTAL_SCORE = 0
DEFAULT_SCORE = 2

pygame.init()

music = pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)


SPACE = pygame.display.set_mode((600,700),0,32)
pygame.display.set_caption("2048")

myfont = pygame.font.SysFont("monospace",20)
scorefont = pygame.font.SysFont("monospace",30)

boardMatrix = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

undoMat =[]

def main(fromLoaded = False):

    if not fromLoaded:
        placeRandomBlock()
        placeRandomBlock()
    printMatrix()


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if checkIfCanGo() == True:
                if event.type == KEYDOWN:
                    if isArrow(event.key):
                        rotations = getRotations(event.key)
                        addToUndo()
                        for i in range(0,rotations):
                            rotateMatrixClockwise()

                        if canMove():
                            moveBlocks()
                            mergeBlocks()
                            placeRandomBlock()

                        for j in range(0,(4-rotations)%4):
                            rotateMatrixClockwise()

                        printMatrix()

            else:
                printGameOver()

            if event.type == KEYDOWN:
                global SIZE_BOARD

                if event.key == pygame.K_SPACE:
                    reset()

                if 50<event.key and 56>event.key:
                    SIZE_BOARD = event.key - 48
                    reset()

                if event.key == pygame.K_s:
                    saveGameState()

                elif event.key == pygame.K_l:
                    loadGameState()

                elif event.key == pygame.K_u:
                    undo()

        pygame.display.update()

#Functions - checking if it is possible to move or not

def canMove():
    for i in range(0,SIZE_BOARD):
        for j in range(1,SIZE_BOARD):
            if boardMatrix[i][j-1] == 0 and boardMatrix[i][j] > 0:
                return True
            elif (boardMatrix[i][j-1] == boardMatrix[i][j]) and boardMatrix[i][j-1] !=0:
                return True
    return False

#Moves the blocks

def moveBlocks():
    for i in range(0,SIZE_BOARD):
        for j in range(0,SIZE_BOARD-1):
            while boardMatrix[i][j] == 0 and sum(boardMatrix[i][j:]) > 0:
                for k in range(j,SIZE_BOARD-1):
                    boardMatrix[i][k] = boardMatrix[i][k+1]
                boardMatrix[i][SIZE_BOARD-1] = 0

# Merge the blocks

def mergeBlocks():
    global TOTAL_SCORE

    for i in range(0,SIZE_BOARD):
        for k in range(0,SIZE_BOARD-1):
            if boardMatrix[i][k] == boardMatrix[i][k+1] and boardMatrix[i][k] !=0:
                boardMatrix[i][k] = boardMatrix[i][k]*2
                boardMatrix[i][k+1] = 0
                TOTAL_SCORE +=boardMatrix[i][k]
                moveBlocks()

# Get a random block

def placeRandomBlock():
    c = 0
    for i in range(0,SIZE_BOARD):
        for j in range(0,SIZE_BOARD):
            if boardMatrix[i][j] == 0:
                c +=1

    k = floor(random() * SIZE_BOARD * SIZE_BOARD)
    print("click")

    while boardMatrix[floor(k/SIZE_BOARD)][k%SIZE_BOARD] != 0:
        k = floor(random() * SIZE_BOARD * SIZE_BOARD)

    boardMatrix[floor(k/SIZE_BOARD)][k%SIZE_BOARD] = 2


# A function for floor value of the given number
def floor(n):
    return int(n - (n %1))

# Printing the matrix

def printMatrix():
    SPACE.fill(PINK)
    global SIZE_BOARD
    global TOTAL_SCORE

    for i in range(0,SIZE_BOARD):
        for j in range(0,SIZE_BOARD):
            pygame.draw.rect(SPACE,getColors(boardMatrix[i][j]), (i*(600/SIZE_BOARD), j*(600/SIZE_BOARD)+100, 600/SIZE_BOARD,600/SIZE_BOARD))
            label = myfont.render(str(boardMatrix[i][j]),1, (WHITE))
            label2 = scorefont.render("Your Score is: " + str(TOTAL_SCORE), 1,(WHITE))
            SPACE.blit(label, (i*(600/SIZE_BOARD)+30, j*(600/SIZE_BOARD)+130))
            SPACE.blit(label2,(75,30))

# Check if can start the moves

def checkIfCanGo():
    for i in range(0,SIZE_BOARD ** 2):
        if boardMatrix[floor(i/SIZE_BOARD)][i%SIZE_BOARD] == 0:
            return True

    for i in range(0,SIZE_BOARD):
        for j in range(0,SIZE_BOARD-1):
            if boardMatrix[i][j] == boardMatrix[i][j+1]:
                return True

            elif boardMatrix[j][i] == boardMatrix[j+1][i]:
                return True
    return False

# Returning a matrix that we can call a list

def convertToLinearMatrix():

    mat = []
    for i in range(0,SIZE_BOARD ** 2):
        mat.append(boardMatrix[floor(i/SIZE_BOARD)][i%SIZE_BOARD])

    mat.append(TOTAL_SCORE)
    return mat

def addToUndo():
    undoMat.append(convertToLinearMatrix())

# Mix up the matrix after a button is pressed

def rotateMatrixClockwise():
    for i in range(0,int(SIZE_BOARD/2)):
        for k in range(i,SIZE_BOARD - i - 1):
            temp1 = boardMatrix[i][k]
            temp2 = boardMatrix[SIZE_BOARD - 1 - k][i]
            temp3 = boardMatrix[SIZE_BOARD - 1 - i][SIZE_BOARD - 1 - k]
            temp4 = boardMatrix[k][SIZE_BOARD - 1 - i]

            boardMatrix[SIZE_BOARD - 1 - k][i] = temp1
            boardMatrix[SIZE_BOARD - 1 - i][SIZE_BOARD - 1 - k] = temp2
            boardMatrix[k][SIZE_BOARD - 1 - i] = temp3
            boardMatrix[i][k] = temp4


#  Game over - when you don't have any places in the matrix or you are out of moves

def printGameOver():
    global TOTAL_SCORE

    SPACE.fill(PINK)

    label = scorefont.render("Game over!", 1, (DEEP_PURPLE))
    label2 = scorefont.render("Your score is: " + str(TOTAL_SCORE), 1, (WHITE))
    label3 = myfont.render("Press 'SPACE' ", 1, (WHITE))
    label4 = myfont.render("to play again!", 1, (WHITE))

    SPACE.blit(label, (50,100))
    SPACE.blit(label2, (50,200))
    SPACE.blit(label3, (50,300))
    SPACE.blit(label4, (50,400))


# Reset the score

def reset():
    global TOTAL_SCORE
    global boardMatrix

    TOTAL_SCORE = 0
    SPACE.fill(PINK)
    boardMatrix = [[0 for i in range(0,SIZE_BOARD)] for j in range(0,SIZE_BOARD)]
    main()

# This saves the state of moves 

def saveGameState():
    f = open("savedata", "w") 

    line1 = " ".join([str(boardMatrix[floor(x/SIZE_BOARD)][x%SIZE_BOARD]) for x in range(0,SIZE_BOARD ** 2)])
    f.write(line1+"\n")
    f.write(str(SIZE_BOARD)+"\n")
    f.write(str(TOTAL_SCORE))
    f.close

# Last move

def undo():
    if len(undoMat) > 0:
        mat = undoMat.pop()
        
        for i in range(0, SIZE_BOARD ** 2):
            boardMatrix[floor(i/SIZE_BOARD)][i%SIZE_BOARD] = mat[i]
        global TOTAL_SCORE
        TOTAL_SCORE = mat[SIZE_BOARD ** 2]

        printMatrix()

def loadGameState():
    global TOTAL_SCORE
    global SIZE_BOARD
    global boardMatrix

    f = open("savedata", "r")

    mat = (f.readline()).split(' ',SIZE_BOARD ** 2)
    SIZE_BOARD = int(f.readline())
    TOTAL_SCORE = int(f.readline())

    for i in range(0,SIZE_BOARD ** 2):
        boardMatrix[floor(i/SIZE_BOARD)][i%SIZE_BOARD] = int(mat[i])

    f.close()

    main(True)


# Defining wich arrow is pressed

def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

def getRotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3


main()




