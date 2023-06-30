##################################
# Backend
##################################

import random
import copy
import itertools

# class method names, hint2 are taken from Sudoku hints: 
# https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15112-3-s23/www/notes/tp-sudoku-hints.html #

class State():
    def __init__(self, board):
        self.board = board
        self.legals = self.inputLegals()
        self.startingLegals()
        self.manualLegals = self.startingCandidates()
        self.initialCells = self.getInitialCells()
        self.selected = None

    def inputLegals(self):
        legals = dict()
        rows, cols = len(self.board), len(self.board[0])
        for row in range(rows):
            legals[row] = dict()
            for col in range(cols):
                legals[row][col] = set(range(1,10))
        return legals
    
    def startingLegals(self):
        rows, cols = len(self.board), len(self.board[0])
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] != 0:
                    self.set(row, col, self.board[row][col])
                    self.legals[row][col] = set()

    def startingCandidates(self):
        manualLegals = dict()
        for row in range(9):
            manualLegals[row] = dict()
            for col in range(9):
                manualLegals[row][col] = set()
        return manualLegals

    def set(self, row, col, value):
        if self.board[row][col] != 0:
            self.unset(row, col)
        if value in self.legals[row][col]:
            self.board[row][col] = value
            for (targetRow, targetCol) in self.getCellRegions(row, col):
                            self.ban(targetRow, targetCol, value)
        else:
            print("Not a Legal Value") #make it so that 
    
    def unset(self, row, col):
        value = self.board[row][col]
        self.board[row][col] = 0
        self.checkLegals()
        self.legals[row][col].add(value)

    def ban(self, row, col, value):
        if value in self.legals[row][col]:
                self.legals[row][col].remove(value)

    def unban(self, row, col, value):
        self.legals[row][col].add(value)

    def checkLegals(self):
        rows, cols = len(self.board), len(self.board[0])
        for row in range(rows):
            for col in range(cols):
                self.legals[row][col] = set(range(1,10))
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] != 0:
                    value = self.board[row][col]
                    self.board[row][col] = 0
                    self.set(row, col, value)

    # hint #
    def hint1(self):
        rows, cols = len(self.board), len(self.board[0])
        targetCells = []
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] == 0 and len(self.legals[row][col]) == 1:
                    targetCells.append((row, col))
        for (targetRow, targetCol) in targetCells:
            for value in list(self.legals[targetRow][targetCol]):
                self.set(targetRow, targetCol, value)      


    def hint2(self):
        for region in self.getAllRegions(): #region = [ (all possible tuples for a cell)]
            for N in range(2, 6):
                result = self.applyRule2(region, N)
                if result != None:
                    return result
        return None

    def applyRule2(self, region, N):
        for tuple in itertools.combinations(region, N): #()
            return 42
        

    def applyRule2(self, region, N):
        cellLegalsInRegion = []
        values = []
        for (row, col) in region:
            if (row, col) not in self.initialCells:
                cellLegals = self.legals[row][col]
                cellLegalsInRegion.append(cellLegals)
        # for all of the combinations of legals in a region
        for combination in itertools.combinations(cellLegalsInRegion, N):
            if containsSameTuples(combination, i=0):
                values = combination[0] #{2, 6, 9}
                for (row, col) in region:
                    for value in values:
                        if (self.legals[row][col] != values and 
                            value in self.legals[row][col]):
                                self.legals[row][col].remove(value)
                        

                #({8, 9}, {8, 9})

    def getBansForAllRegions(self, values, targets):
        # The values (to ban) can stay in the targets, but they must be
        # banned from all other cells in all regions that contain all
        # the targets
        bans = [ ]
        for region in self.getAllRegionsThatContainTargets(targets):
            target = [(row, col), (row, col)]
    
    # def getAllRegionsThatContainTargets(self)


    def valuesAreOnlyLegals(self, values, targets):
        for target in targets:
            row, col = target
            if not self.legals[row][col].issubset(values):
                return False
        return True

    def getBansForAllRegions(self, values, targets):
        bans = []
        for region in self.getAllRegionsThatContainTargets(targets):
            for cell in region:
                row, col = cell
                if cell not in targets:
                    for value in values:
                        if value in self.legals[row][col]:
                            bans.append((row, col, value))
        return bans if bans else None

    # compute regions #
    def getRowRegion(self, row):
        cols = len(self.board[0])
        rowRegion = []
        for col in range(cols):
            rowRegion.append((row, col))
        return rowRegion

    def getColRegion(self, col):
        rows = len(self.board)
        colRegion = []
        for row in range(rows):
            colRegion.append((row, col))
        return colRegion
    
    def getBlockRegion(self, block):
        blockRegion = []
        block -= 1
        for row in range((block//3) * 3, (block//3) * 3 + 3):
            for col in range((block % 3)*3, (block % 3)*3 + 3):
                blockRegion.append((row, col))
        return blockRegion

    def getBlock(self, row, col):
        return 3 * (row // 3) + col // 3 + 1
    
    def getBlockRegionByCell(self, row, col):
        return self.getBlockRegion(self.getBlock(row, col))
    
    def getCellRegions(self, row, col):
        rowSet = set(self.getRowRegion(row))
        colSet = set(self.getColRegion(col))
        blockSet = set(self.getBlockRegionByCell(row, col))
        cellRegionsSet = rowSet | colSet | blockSet
        cellRegionsList = sorted(list(cellRegionsSet))
        return cellRegionsList
    
    def getAllRegions(self):
        rows, cols = len(self.board), len(self.board[0])
        allRegions = []
        for row in range(rows):
            for col in range(cols):
                allRegions.append(self.getCellRegions(row, col))
        return allRegions
    
    def getAllRegionsThatContainTargets(self, targets):
        targetRegions = []
        for (row, col) in self.getAllRegions():
            if self.board[row][col] == targets:
                targetRegions.append((row,col))
        return targetRegions
    
    def getInitialCells(self):
        rows, cols = len(self.board), len(self.board[0])
        cellList = []
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] != 0:
                    cellList.append((row, col))
        return cellList

    # backtracking #
    def backtracker(self):
        if self.checkGameOver():
            return self.board
        else:
            (row, col) = self.leastLegal()
            for value in list(self.legals[row][col]):
                self.set(row, col, value)
                if self.isLegal():
                    solution = self.backtracker()
                    if solution != None:
                        return solution
                self.unset(row, col)
            return None

                
    def checkGameOver(self):
        for row in self.board:
            if 0 in row:
                return False
        return True
    
    def isLegal(self):
        rows, cols = len(self.board), len(self.board[0])
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] == 0 and len(self.legals[row][col]) == 0:
                    return False
        return True
        
    def leastLegal(self):
        rows, cols = len(self.board), len(self.board[0])
        least = 9
        leastCell = None
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] == 0 and len(self.legals[row][col]) < least:
                    least = len(self.legals[row][col])
                    leastCell = (row, col)
                else:
                    continue
        return leastCell

    # print for debugging #

    # copied from TP Overview
    def printBoard(self):
        print2dList(self.board)

    def printLegals(self):
        colWidth = 4
        for col in range(9):
            colWidth = max(colWidth, 1+max([len(self.legals[row][col]) for row in range(9)]))
        for row in range(9):
            for col in range(9):
                label = ''.join([str(v) for v in sorted(self.legals[row][col])])
                if label == '': label = '-'
                print(f"{' '*(colWidth - len(label))}{label}", end='')
            print()
    
    def print(self): self.printBoard(); self.printLegals()



##################################
# Backend Helper
##################################

def readFile(path):
    with open(path, "rb") as f:
        return f.read().decode('utf-8')

def chooseBoard(difficulty):
    if difficulty == 'easy' or difficulty == 'medium' or difficulty == 'hard':
        choice = randrange(1, 50)
    elif difficulty == 'evil' or difficulty == 'expert':
        choice = randrange(1, 25)
    
    # if choice >= 10:
    #     board = readFile(f"C:\\Users\\jaeha\\Desktop\\tp2sudoku\\sudoku\\tp-starter-files\\boards\\{difficulty}-{choice}.png.txt")
    # else:
    #     board = readFile(f"C:\\Users\\jaeha\\Desktop\\tp2sudoku\\sudoku\\tp-starter-files\\boards\\{difficulty}-0{choice}.png.txt")

    if choice >= 10:
            board = readFile(f"/Users/alina/Desktop/sudoku/tp-starter-files/boards/{difficulty}-{choice}.png.txt")
    else:
        board = readFile(f"/Users/alina/Desktop/sudoku/tp-starter-files/boards/{difficulty}-0{choice}.png.txt")
    return board

def make2dBoard(board):
    # board = board.splitlines()
    board = [line.decode('utf-8') for line in board.splitlines()]
    finalBoard = []
    for line in board:
        lineList = line.split(' ')
        intList = []
        for string in lineList:
            intList.append(int(string))
        finalBoard.append(intList)
    return finalBoard

#copied from TP hints
def print2dList(L):
        print(repr2dList(L))

def repr2dList(L):
        if (L == []): return '[]'
        output = [ ]
        rows = len(L)
        cols = max([len(L[row]) for row in range(rows)])
        M = [['']*cols for row in range(rows)]
        for row in range(rows):
            for col in range(len(L[row])):
                M[row][col] = repr(L[row][col])
        colWidths = [0] * cols
        for col in range(cols):
            colWidths[col] = max([len(M[row][col]) for row in range(rows)])
        output.append('[\n')
        for row in range(rows):
            output.append(' [ ')
            for col in range(cols):
                if (col > 0):
                    output.append(', ' if col < len(L[row]) else '  ')
                output.append(M[row][col].rjust(colWidths[col]))
            output.append((' ],' if row < rows-1 else ' ]') + '\n')
        output.append(']')
        return ''.join(output)

def containsSameTuples(combination, i=0):
        #({3, 6, 7}, {3, 6，7}, {3, 6, 7})
        if len(combination[i]) != len(combination):
            return False
        if i == len(combination)-1:
            return combination[i] == combination[i-1]
        else:
            return (combination[i+1] == combination[i] and 
                    containsSameTuples(combination, i+1))

##################################
# App
##################################

from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    print('In onAppStart')
    app.state = None
    app.initialState = None
    app.gameOver = True
    app.selected = None


def onAppStop(app):
    print('In onAppStop')

##################################
# Splash
##################################

'''
Citation: read file and load images from term project notes
https://www.cs.cmu.edu/~112-3/notes/term-project.html
'''

def readFile(path):
    with open(path, "rb") as f:
        return f.read()

def splash_onAppStart(app):
    print('In splash_onAppStart')
    app.color = 'gold'
    app.activatedCounter1 = 0
    app.splashImage = Image.open('splash.jpg')
    app.splashImage = CMUImage(app.splashImage)
    app.difficulty = None

def splash_onScreenActivate(app):
    print('In screen1_onScreenActivate')

def splash_redrawAll(app):
    splash_image = Image.open('splash.jpg')
    drawImage(app.splashImage, 0, 0, 
              width=app.width, height=app.height)

def splash_onMousePress(app, mouseX, mouseY):
    left, top = app.width//2, 0
    width, height = 257, 162
    if (left < mouseX < left + width):
        number = mouseY // 162
        if number == 0:
            app.difficulty = 'easy'
        elif number == 1:
            app.difficulty = 'medium'
        elif number == 2:
            app.difficulty = 'hard'
        elif number == 3:
            app.difficulty = 'expert'
        elif number == 4:
            app.difficulty = 'evil'
        app.gameOver = False
        app.selected = None
        board = make2dBoard(chooseBoard(app.difficulty))
        restart(app)
        app.state = State(board)
        app.initialCells = app.state.getInitialCells()
        setActiveScreen('playScreen')
        # solution board #
        solutionBoard = copy.deepcopy(app.state.board)
        solutionState = State(solutionBoard)
        solutionState.backtracker()
        app.solution = solutionState.board

##################################
# Play Screen
##################################

def playScreen_onAppStart(app):
    print('In playScreen_onAppStart')
    app.cx = app.width/2
    app.dx = 10

    beige = rgb(240, 235, 220)
    app.fill = beige

    lightYellow = rgb(238, 227, 195)
    app.filledColor = app.fill

    yellow = rgb(242, 209, 111)
    app.selectedColor = yellow

    grey = rgb(238, 227, 195)
    app.presetColor = grey

    red = rgb(236, 46, 49)
    app.redDotColor = red

    # top bar
    app.backImage = Image.open('back.png')
    app.backImage = CMUImage(app.backImage)
    app.helpImage = Image.open('help.png')
    app.helpImage = CMUImage(app.helpImage)

    # board attributes
    app.rows = 9
    app.cols = 9
    app.boardLeft = 250
    app.boardTop = 100
    app.boardWidth = app.width-600
    app.boardHeight = app.height-200
    app.cellBorderWidth = 0.5
    app.cellColor = [([app.fill] * app.cols) for row in range(app.rows)]
    app.board = [([None] * app.cols) for row in range(app.rows)]

    # number pad attributes
    app.padLeft = app.boardLeft + app.boardWidth + 20
    app.padTop = app.boardTop + app.boardHeight + 10
    
    for row in range (app.rows):
        for col in range (app.cols):
            if not app.gameOver:
                if app.state.board[row][col] != 0:
                    app.cellColor[row][col] = app.filledColor
                else:
                    app.cellColor[row][col] = app.fill

    restart(app)

def restart(app):
    if app.selected != None:
        prevRow, prevCol = app.selected
        app.cellColor[prevRow][prevCol] = app.fill
    app.selected = None
    app.numInput = None
    app.numInputRow, app.numInputCol = None, None
    app.displayHelp = False
    app.displayGameOver = False
    app.autoCandidate = False
    app.normalMode = True
    app.wrongValCells = []


def playScreen_onScreenActivate(app):
    print('In playScreen_onScreenActivate')

def playScreen_onMousePress(app, mouseX, mouseY):
    ##### check for the (row, col) that is selected on the board #####
    if ((mouseX >= app.boardLeft and mouseX <= app.boardLeft+app.boardWidth) and
        (mouseY >= app.boardTop and mouseY <= app.boardTop+app.boardHeight)):
        cellWidth, cellHeight = getCellSize(app)
        ##### restore previous selected cell to white #####
        if app.selected != None:
            prevSelectedRow, prevSelectedCol = app.selected
            app.cellColor[prevSelectedRow][prevSelectedCol] = app.fill
        selectedRow = int((mouseY-app.boardTop) // cellHeight)
        selectedCol = int((mouseX-app.boardLeft) // cellWidth)
        app.cellColor[selectedRow][selectedCol] = app.selectedColor
        app.selected = (selectedRow, selectedCol)

    ##### check for the number that is selected on the number pad #####
    numCellLeft, numCellTop = getNumCellLeftTop(app, 0, 0)
    cellWidth, cellHeight = getCellSize(app)
    if app.selected != None:
        if ((mouseX >= numCellLeft and mouseX <= numCellLeft+cellWidth*3+30) and
            (mouseY >= numCellTop and mouseY <= numCellTop+cellWidth*3+30)):
            if not ((967 <= mouseX <= 982) or (1048 <= mouseX <= 1063) or
                (223<= mouseY <= 238) or (305<= mouseY <= 320)):
                x = mouseX - 900
                y = mouseY - 157
                row = y // (cellHeight+7)
                col = x // (cellWidth+7)
                # app.selectedNumRow 
                num = row*3 + col+1
                app.numInput = num
    
    if app.state.checkGameOver():
        print('gameOvercheck:')
        app.gameOver = True

    # if an empty cell is selected and an number is inputted
    if app.selected != None and app.numInput != None:
        row, col = app.selected
        ##### if normal mode: display selected number #####
        if app.normalMode:
            # set the number if the number input is legal
            if app.numInput in app.state.legals[row][col]:
                app.state.set(row, col, app.numInput)
                if app.numInput != app.solution[row][col]:
                    app.wrongValCells.append(app.selected)
                else:
                    if (row, col) in app.wrongValCells:
                        # print('enter')
                        app.wrongValCells.remove((row, col))
                app.numInput = None
            #check for gameOver condition
            print(app.state.checkGameOver())
            if app.state.checkGameOver():
                app.gameOver = True
        ##### if manual mode: display selected legal #####
        else:
            app.state.manualLegals[row][col].add(int(app.numInput))
            app.numInput = None

    ##### check top bar click #####
    barLeft, barTop = getNumCellLeftTop(app, 0, 0)
    barTop = app.boardTop
    if (mouseY >= barTop and mouseY <= barTop+44):
        # if clicked on normal:
        if (mouseX >= barLeft and mouseX <= barLeft+116):
            app.normalMode = True
        # if clicked on candidate:
        elif (mouseX >= barLeft+116 and mouseX <= barLeft+232):
            app.normalMode = False

    ##### check cancel box click #####
    #900, 402 # 1130, 453
    if ((mouseX >= 900 and mouseX <= 1130) and
        (mouseY >= 402 and mouseY <= 453)):
        if app.selected != None:
            selectedRow, selectedCol = app.selected
            if app.state.board[selectedRow][selectedCol] != 0:
                num = app.state.board[selectedRow][selectedCol]
                app.state.unset(selectedRow, selectedCol)
            if (selectedRow, selectedCol) in app.wrongValCells:
                app.wrongValCells.remove((selectedRow, selectedCol))

    ##### check for back button #####
    if ((mouseX >= 95 and mouseX <= 95+55) and
        (mouseY >= 29 and mouseY <= 29+15)):
        # app.gameOver = True
        restart(app)
        setActiveScreen('splash')
    
    ##### check for help button #####
    if ((mouseX >= 1100 and mouseX <= 1100+26) and
        (mouseY >= 27 and mouseY <= 27+26)):
        # setActiveScreen('help')
        app.displayHelp = True

    if ((mouseX >= 880 and mouseX <= 950) and
        (mouseY >= 130 and mouseY <= 190)) and app.displayHelp:
        app.displayHelp = False

    ##### check for auto candidate mode #####
    checkBoxLeft, checkBoxTop = getNumCellLeftTop(app, 0, 0)
    checkBoxTop += (cellHeight*3 + 30) + 85
    if ((mouseX >= checkBoxLeft and mouseX <= checkBoxLeft+15) and
        (mouseY >= checkBoxTop and mouseY <= checkBoxTop+15)):
        app.autoCandidate = not app.autoCandidate

    ##### check for hint 1 #####
    if ((mouseX >= 900 and mouseX <= 1130) and
        (mouseY >= 582 and mouseY <= 633)):
        print('clicked')
        app.state.hint1()

    ##### check for hint 2 #####
    if ((mouseX >= 900 and mouseX <= 1130) and
        (mouseY >= 648 and mouseY <= 699)):
        app.state.hint2()
    
    if app.gameOver:
        setActiveScreen('gameOver')
        # drawGameOver(app)

def playScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.fill)
    drawImage(app.backImage, 95, 25, width=55, height=15)
    drawImage(app.helpImage, 1100, 20, width=26, height=26)
    drawLabel(app.difficulty.upper(), app.width/2, 31, size=20, bold=True)
    drawBoard(app)
    drawPad(app)
    drawBoardBorder(app)
    drawNum(app, app.state.board)

    drawLegals(app)

    for (row, col) in app.wrongValCells:
        drawDot(app, row, col)
    
    drawHelp(app)

    if app.gameOver:
        setActiveScreen('gameOver')


'''
Citation: draw board functions from Tetris project
https://cs3-112-f22.academy.cs.cmu.edu/exercise/4969
'''

def drawHelp(app):
    helpImage =  Image.open('helpScreen.png')
    helpImage = CMUImage(helpImage)
    if app.displayHelp:
        drawImage(helpImage, 230, 130, width=720, height=580)
        

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Draw Number Pad ~~~~~~~~~~~~~~~~~~~~~~~~~~ # (9)

def drawPad(app):
    cellWidth, cellHeight = getCellSize(app)

    for row in range(3):
        for col in range(3):
            ##### draw number cells #####
            drawNumCell(app, row, col, app.fill)
            numCellLeft, numCellTop = getNumCellLeftTop(app, row, col)
            ##### draw numbers #####
            drawLabel((row+(col+row*2))+1, 
                        numCellLeft + (cellWidth)/2, 
                        numCellTop + (cellHeight)/2, 
                        size=30, bold=True)

    ##### draw cancel box #####
    boxLeft, boxTop = getNumCellLeftTop(app, 0, 0)
    boxTop += (cellHeight*3 + 30) + 15

    drawRect(boxLeft, boxTop,
             cellWidth*3+30, cellHeight//1.3, fill=app.fill, 
             border='black', borderWidth = app.cellBorderWidth)
    drawLabel('x', boxLeft+(cellWidth*3+30)//2, boxTop+cellHeight//2.6, 
              size=30, bold=True)

    ###### draw auto candidate option #####
    checkBoxLeft, checkBoxTop = getNumCellLeftTop(app, 0, 0)
    checkBoxTop += (cellHeight*3 + 30) + 85
    if app.autoCandidate:
        drawRect(checkBoxLeft, checkBoxTop, 15, 15, fill=app.selectedColor,
                 border='black', borderWidth=0.5)
    else:
        drawRect(checkBoxLeft, checkBoxTop, 15, 15, fill=None,
                border='black', borderWidth=0.5)
    drawLabel('Auto Candidate Mode', checkBoxLeft+100, checkBoxTop+7, size=16)

    ##### draw hint boxes #####
    ## Hint 1 ##
    cellLeft1, cellTop1 = getCellLeftTop(app, 7, 8)
    hintBoxTop1 = cellTop1 + 15
    drawRect(boxLeft, hintBoxTop1,
             cellWidth*3+30, cellHeight//1.3, fill=app.fill, 
             border='black', borderWidth = app.cellBorderWidth)
    drawLabel('Auto-Fill Naked Singles', 
              boxLeft+(cellWidth*3+30)//2, hintBoxTop1+cellHeight//2.6, size=16)
    ## Hint 2 ##
    cellLeft2, cellTop2 = getCellLeftTop(app, 8, 8)
    hintBoxTop2 = cellTop2 + 15
    drawRect(boxLeft, hintBoxTop2,
             cellWidth*3+30, cellHeight//1.3, fill=app.fill, 
             border='black', borderWidth = app.cellBorderWidth)
    drawLabel('Remove Naked Tuples', 
              boxLeft+(cellWidth*3+30)//2, hintBoxTop2+cellHeight//2.6, size=16)
    

    ##### draw top bar #####
    barLeft, barTop = getNumCellLeftTop(app, 0, 0)
    barTop = app.boardTop
    ## Normal Button ##
    if app.normalMode:
        normalFill = 'black'
        normalTextFill = app.fill
        candidateFill = app.fill
        candidateTextFill = 'black'
    else:
        normalFill = app.fill
        normalTextFill = 'black'
        candidateFill = 'black'
        candidateTextFill = app.fill
    drawRect(barLeft, app.boardTop,
             (cellWidth*3+30)//2+1, cellHeight//1.5, fill=normalFill, 
             border='black', borderWidth = app.cellBorderWidth)
    drawLabel('Normal', barLeft+(cellWidth*3+30)//4, barTop+cellHeight//3,
              size=16, fill=normalTextFill)
    ## Candidate Button ##
    drawRect(barLeft+(cellWidth*3+30)//2, app.boardTop,
             (cellWidth*3+30)//2, cellHeight//1.5, fill=candidateFill, 
             border='black', borderWidth = app.cellBorderWidth)
    drawLabel('Candidate', barLeft+(cellWidth*3+30)//4 + (cellWidth*3+30)//2+1, 
              barTop+cellHeight//3,
              size=16, fill=candidateTextFill)


def drawNumCell(app, row, col, color):
    numCellLeft, numCellTop = getNumCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(numCellLeft, numCellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getNumCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    numCellLeft = app.boardLeft + app.boardWidth + col * cellWidth + 50 + col*15
    numCellTop = app.boardTop + row * cellHeight + (cellHeight - 10) + row*15
    return (numCellLeft, numCellTop)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Draw Board ~~~~~~~~~~~~~~~~~~~~~~~~~~ # 

def drawBoard(app):
    # background color
    # drawRect(0, 0, app.width, app.height, fill=app.pieceColor, opacity=50)
    # draw board
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=app.fill)
    ##### draw cells #####
    if app.selected != None:
        selectedRow, selectedCol = app.selected
    for row in range(app.rows):
        for col in range(app.cols):
            if app.selected != None and (row, col) == (selectedRow, selectedCol):
                color = app.selectedColor
            elif app.state.board[row][col] != 0:
                color = app.filledColor
            else:
                color = app.cellColor[row][col]
            drawCell(app, row, col, color)
    ##### draw blocks #####
    for row in range (app.rows//3):
        for col in range (app.cols//3):
            color = app.board[row][col]
            drawBlock(app, row, col, color)


def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
               fill=None, border='black',
               borderWidth=8*app.cellBorderWidth)

def drawNum(app, board):
    cellWidth, cellHeight = getCellSize(app)
    numLeft = app.boardLeft + cellWidth//2
    numTop = app.boardTop + cellHeight//2
    for row in range (9):
        for col in range (9):
            num = board[row][col]
            if num != 0:
                drawLabel(num, numLeft+col*cellWidth, numTop+row*cellHeight,
                        size=35, bold=True)

def drawDot(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawCircle(cellLeft+(cellWidth*0.8), cellTop+(cellHeight*0.8), 8, 
               fill=app.redDotColor)

def drawLegals(app):
    for row in range (9):
        for col in range (9):
            # ignore the preset cells
            if (row, col) not in app.initialCells: 
                if app.state.board[row][col] == 0:
                    if app.autoCandidate:
                        legals = app.state.legals[row][col] # a set
                    else:
                        legals = app.state.manualLegals[row][col]
                    drawCellLegals(app, row, col, legals)

def drawCellLegals(app, row, col, legals):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    for legal in legals:
        left, top = cellLeft, cellTop
        if legal % 3 == 1:
            left += 10
        elif legal % 3 == 2:
            left += cellWidth//2
        elif legal % 3 == 0:
            left += cellWidth - 10
        if legal < 4:
            top += 12
        elif legal < 7:
            top += cellWidth//2 
        elif legal < 10:
            top += cellWidth - 12
        
        drawLabel(legal, left, top, size=14, fill='grey', opacity=70)
        

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if (row, col) in app.initialCells: #!!! making initial cell/input cell diff !!!
        color = app.presetColor
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    # cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellWidth)

def drawBlock(app, row, col, color):
    blockLeft, blockTop = getBlockLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    blockWidth, blockHeight = cellWidth * 3, cellHeight * 3
    drawRect(blockLeft, blockTop, blockWidth, blockHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth*4)

def getBlockLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    blockWidth, blockHeight = cellWidth * 3, cellHeight * 3
    blockLeft = app.boardLeft + col * blockWidth
    blockTop = app.boardTop + row * blockHeight
    return (blockLeft, blockTop)

##################################
# help
##################################

def onAppStart(app):
    print('In onAppStart')
    app.state = None
    app.initialState = None
    app.gameOver = True
    app.selected = None


def onAppStop(app):
    print('In onAppStop')

##################################
# Game Over
##################################

def gameOver_onAppStart(app):
    gameOverImage = Image.open('gameOver.png')
    app.gameOverImage = CMUImage(gameOverImage)

def gameOver_redrawAll(app):
    drawImage(app.gameOverImage, 0, 0, 
              width=app.width, height=app.height)

def gameOver_onMousePress(app, mouseX, mouseY):
    if ((900 <= mouseX <= 1140) and (650 <= mouseY <= 750)):
        setActiveScreen('splash')


##################################
# main
##################################


def main():
    runAppWithScreens(initialScreen='splash', width=1200, height=800)

main()