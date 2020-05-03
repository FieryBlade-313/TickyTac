import pygame
import thorpy
import math
import random


class IdentifierText:
    def __init__(self, x, y, content, col=(0, 0, 0), bcol=(255, 255, 255)):
        self.content = content
        self.text = font.render(
            str(content), True, col, bcol)
        self.textRect = self.text.get_rect()
        self.x = x
        self.y = y
        self.textRect.center = (x, y)

    def draw(self):
        screen.blit(self.text, self.textRect)

    def updateColor(self, col, bcol):
        self.col = col
        self.bcol = bcol
        self.text = font.render(
            str(self.content), True, col, bcol)

    def isClicked(self, pos):
        return abs(pos[0]-self.x) <= self.textRect.width and abs(pos[1] - self.y) <= self.textRect.height


class valText:
    def __init__(self, x, y, content):
        self.content = content
        self.text = self.textChild = font.render(
            str(content), True, (0, 0, 0), (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)

    def draw(self):
        screen.blit(self.text, self.textRect)

    def updateContent(self, content):
        self.content = content
        self.text = self.textChild = font.render(
            str(content), True, (0, 0, 0), (255, 255, 255))


class moverCircle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.size)

    def isClicked(self, pos):
        return math.sqrt((pos[0]-self.x)**2+(pos[1]-self.y)**2) < self.size


class Slider:
    def __init__(self, x, y, length, minVal, maxVal, identifier):
        self.x = x
        self.y = y
        self.length = length
        self.width = 10
        self.minVal = minVal
        self.maxVal = maxVal
        self.val = minVal
        self.child = moverCircle(self.x, self.y+self.width//2, 15)
        self.textChild = valText(
            self.x + self.length//2, self.y - self.width*2.5, self.val)
        self.identifierText = IdentifierText(
            self.x+self.length//2, self.y - self.width*8, identifier)

    def computeVal(self):
        self.val = ((self.maxVal - self.minVal) *
                    (self.child.x-self.x)) // self.length + self.minVal

    def draw(self):
        pygame.draw.rect(screen, (180, 180, 180),
                         (self.x, self.y, self.length, self.width))
        self.child.draw()
        self.textChild.draw()
        self.identifierText.draw()

    def isClicked(self, pos):
        return abs(pos[0]-self.x) <= self.length and abs(pos[1] - self.y) <= self.width

    def updateText(self):
        self.textChild.updateContent(self.val)


class Places:
    def __init__(self, x, y, board):
        self.child = None
        self.index = y*board.size + x
        self.size = board.length / (board.size+1)
        self.padding = self.size/(board.size+1)
        self.x = x*(self.size+self.padding) + board.x
        self.y = y*(self.size+self.padding) + board.y

    def isClicked(self, pos):
        return abs(self.x - pos[0]) < self.size and abs(self.y - pos[1]) < self.size

    def __str__(self):
        print(self.x, self.y, self.size)

    def draw(self):
        color = (150, 150, 150)
        if self.child == 'x':
            color = (128, 206, 82)
        elif self.child == 'o':
            color = (64, 130, 151)
        pygame.draw.rect(screen, color,
                         (self.x, self.y, self.size, self.size))


class Board:
    def __init__(self, size, winLength, length, windowLength):
        self.size = size
        self.x = windowLength/2 - length/2
        self.y = self.x
        self.winLength = winLength
        self.board = []
        self.length = length
        self.empty = 0
        self.first = 1
        self.second = -1
        self.places = []
        self.createBoard()

    def createBoard(self):
        for i in range(self.size):
            self.board.append([])
            for j in range(self.size):
                self.places.append(Places(j, i, self))
                self.board[i].append(self.empty)

    def placeObject(self, pos, isFirst):
        self.board[pos[1]][pos[0]] = self.first if isFirst else self.second
        # print(pos[1]*self.size+pos[0])
        self.places[pos[1]*self.size+pos[0]].child = 'x' if isFirst else 'o'

    def viewBoard(self):
        for i in range(self.size):
            print(self.board[i])

    def draw(self):
        for place in self.places:
            place.draw()

    def convertToString(self):
        str = ""
        for i in range(self.size):
            for j in range(self.size):
                c = '*'
                if self.board[i][j] == 1:
                    c = 'x'
                elif self.board[i][j] == -1:
                    c = 'o'
                str = str+c

        return str

    def getClicked(self, pos):
        for place in self.places:
            if place.isClicked(pos):
                return place if place.child == None else None
        return None


def checkComplete(state, pos):
    # print(state, pos)
    c = state[pos[0]*board.size+pos[1]]
    # print(c)
    if c == '*':
        return False
    row = col = diag1 = diag2 = True
    if pos[0]+board.winLength <= board.size and pos[1]+board.winLength <= board.size:
        # print("Diag1")
        for k in range(board.winLength):
            y = pos[0]+k
            x = pos[1]+k
            # print(y, x)
            if diag1 and state[y*board.size+x] != c:
                diag1 = False
                break
    else:
        diag1 = False
    # print(pos[0] + board.winLength, pos[1]-board.winLength)
    if pos[0] + board.winLength <= board.size and pos[1]-board.winLength+1 > -1:
        # print("Diag2")
        for k in range(board.winLength):
            y = pos[0]+k
            x = pos[1]-k
            # print(y, x, y*board.size+x, state[y*board.size+x])
            if diag2 and state[y*board.size+x] != c:
                diag2 = False
                break
    else:
        diag2 = False
    if pos[1]+board.winLength <= board.size:
        # print("Row")
        for x in range(pos[1], pos[1]+board.winLength):
            # print(pos[0], x)
            if row and state[pos[0]*board.size+x] != c:
                row = False
                break
    else:
        row = False
    if pos[0] + board.winLength <= board.size:
        # print("Col")
        for y in range(pos[0], pos[0]+board.winLength):
            # print(y, pos[1], y*board.size+pos[1], state[y*board.size+pos[1]])
            if col and state[y*board.size+pos[1]] != c:
                col = False
                break
    else:
        col = False

    return diag1 or diag2 or row or col


def isTerminal(state):
    if '*' not in state:
        return (True, 0)
    for i in range(board.size):
        for j in range(board.size):
            res = checkComplete(state, (i, j))
            if res:
                return (True, 1 if state[i*board.size+j] == 'x' else 2)
    return (False, None)


def getStateValue(state):
    mult = 3
    max_Multiplier = 12
    for i in range(board.size):
        for j in range(board.size):
            if checkComplete(state, (i, j)):
                return 1000 if state[i*board.size+j] == 'x' else -1000
    score = 0
    for i in range(board.size-board.winLength+1):
        for j in range(board.size-board.winLength+1):
            multiplier = [1, 1, 1]
            prevChar = ['*', '*', '*']

            for k in range(board.winLength):

                x = i+k
                y = j+k

                exceptedMultiplier = [False, False, False]

                if prevChar[0] == state[y*board.size + x] and prevChar[0] != '*' and multiplier[0] < max_Multiplier:
                    multiplier[0] = multiplier[0]*mult
                elif multiplier[0] != 1 and prevChar[0] != '*':
                    exceptedMultiplier[0] = True
                else:
                    multiplier[0] = 1
                if prevChar[1] == state[i*board.size + x] and prevChar[1] != '*' and multiplier[0] < max_Multiplier:
                    multiplier[1] = multiplier[1]*mult
                elif multiplier[1] != 1 and prevChar[1] != '*':
                    exceptedMultiplier[1] = True
                else:
                    multiplier[1] = 1
                if prevChar[2] == state[y*board.size + j] and prevChar[2] != '*' and multiplier[0] < max_Multiplier:
                    multiplier[2] = multiplier[2]*mult
                elif multiplier[2] != 1 and prevChar[2] != '*':
                    exceptedMultiplier[2] = True
                else:
                    multiplier[2] = 1

                sign = [0, 0, 0]
                if state[y*board.size + x] == 'x':
                    sign[0] = 1
                elif state[y*board.size + x] == 'o':
                    sign[0] = -1

                if state[i*board.size + x] == 'x':
                    sign[1] = 1
                elif state[i*board.size + x] == 'o':
                    sign[1] = -1

                if state[y*board.size + j] == 'x':
                    sign[2] = 1
                elif state[y*board.size + j] == 'o':
                    sign[2] = -1

                for index in range(3):
                    score = score + sign[index]*multiplier[index]*1
                    if exceptedMultiplier[index]:
                        multiplier[index] = False

                prevChar[0] = state[y*board.size + x]
                prevChar[1] = state[i*board.size + x]
                prevChar[2] = state[y*board.size + j]

    return score


def minimaxAB(state, depth, remPlaces, maximizingPlayer, alpha=-math.inf, beta=math.inf, AlphaBeta=False, Heuristic=False):
    # print(state)
    if (Heuristic and depth == HeuDepth) or remPlaces == 0 or isTerminal(state)[0]:
        # if state[0:4] == 'x**x':
        #     print(state)
        return (0, getStateValue(state))

    if maximizingPlayer:
        maxEval = -math.inf
        maxIndex = 0
        for i in range(len(state)):
            if state[i] == '*':
                tState = state[0:i]+'x'+state[i+1:]
                eval = minimaxAB(tState, depth+1, remPlaces-1, False,
                                 alpha, beta, AlphaBeta, Heuristic)[1]
                if eval > maxEval:
                    maxEval = eval
                    maxIndex = i
                if AlphaBeta:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return (maxIndex, maxEval)
    else:
        minEval = math.inf
        minIndex = 0
        for i in range(len(state)):
            if state[i] == '*':
                tState = state[0:i]+'o'+state[i+1:]
                eval = minimaxAB(tState, depth+1, remPlaces-1, True,
                                 alpha, beta, AlphaBeta, Heuristic)[1]
                if eval < minEval:
                    minEval = eval
                    minIndex = i
                if AlphaBeta:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return (minIndex, minEval)


def Draw():
    # print("drawing")
    screen.fill((255, 255, 255))
    if menuPhase:
        for item in menuItems:
            item.draw()
    elif sliderPhase:
        for index, slider in enumerate(sliders):
            if menuResult[1] or index != 2:
                slider.draw()
        button.draw()
    elif colorPhase:
        for item in colorItems:
            item.draw()
    else:
        # p2.printDetail()
        board.draw()
        winText.draw()
    pygame.display.flip()


def SelectingMenuPhase():
    global menuPhase
    global running
    while menuPhase and running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                menuPhase = False
                running = False
                return (False, False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, item in enumerate(menuItems):
                    if item.isClicked(pos):
                        menuPhase = False
                        return (responseList[index])

            for item in menuItems:
                if item.isClicked(pos):
                    item.updateColor((255, 255, 255), (0, 0, 0))
                else:
                    item.updateColor((0, 0, 0), (255, 255, 255))

        Draw()


def SelectingSliderPhase():
    global sliderPhase
    global running
    selected = None
    while sliderPhase and running:
        # print(selected.val)
        sliders[1].maxVal = sliders[0].val
        pos = pygame.mouse.get_pos()
        if selected != None and isMoved:
            if sliders[0] == selected:
                sliders[1].computeVal()
                sliders[1].updateText()
            selected.updateText()
            selected.child.x = pos[0] if pos[0] - \
                selected.x <= selected.length and pos[0] > selected.x else selected.child.x
            selected.computeVal()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sliderPhase = False
                running = False
                return (3, 3, 3)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for slider in sliders:
                    if slider.isClicked(pos) or slider.child.isClicked(pos):
                        isMoved = True
                        selected = slider
                if button.isClicked(pos):
                    sliderPhase = False
                    return (sliders[0].val, sliders[1].val, sliders[2].val)
            if event.type == pygame.MOUSEBUTTONUP:
                isMoved = False
                selected = None
            if button.isClicked(pos):
                button.updateColor((255, 255, 255), (0, 0, 0))
            else:
                button.updateColor((0, 0, 0), (255, 255, 255))

        Draw()


def SelectingColorToPlay():
    global colorPhase
    global running
    while colorPhase and running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                colorPhase = False
                running = False
                return (False, False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, item in enumerate(colorItems):
                    if item.isClicked(pos):
                        colorPhase = False
                        return (index == 0)

            for item in colorItems:
                if item.isClicked(pos):
                    item.updateColor((255, 255, 255), (0, 0, 0))
                else:
                    item.updateColor((0, 0, 0), (255, 255, 255))

        Draw()


pygame.init()
length = 600

font = pygame.font.Font('darkforest.ttf', 25)
screen = pygame.display.set_mode((length, length))
pygame.display.set_caption("Tic-Tac-Toe")


menuItems = [IdentifierText(300, 150, "Basic MinMax"),
             IdentifierText(300, 250, "Alpha Beta Pruning"), IdentifierText(300, 350, "Depth Limited Minmax"), IdentifierText(300, 450, "Alpha Beta Pruning with Depth Limited")]
responseList = [(False, False), (True, False), (False, True), (True, True)]

running = True
menuPhase = True
menuResult = SelectingMenuPhase()
print(menuResult)

sliders = [Slider(100, 100, 300, 3, 12, "Size"), Slider(
    150, 250, 200, 3, 10, "Continuous Elements(for Winning)"), Slider(200, 400, 100, 3, 7, "Depth to Search(Heuristics)")]

button = IdentifierText(250, 450, "Confirm")


isMoved = False
sliderPhase = True
sliderResult = None

sliderResult = SelectingSliderPhase()

HeuDepth = sliderResult[2] if running else None
board = Board(sliderResult[0], sliderResult[1],
              400, length) if running else None

colorItems = [IdentifierText(300, 200, "Play First"),
              IdentifierText(300, 400, "Play Second")]

colorPhase = True
colorResult = SelectingColorToPlay()


firstTurn = True
remPieces = board.size**2 if running else None
gameOver = False
isPlayWhite = colorResult if running else None
winName = ["Tie", "You Won", "Computer Won"] if isPlayWhite else [
    "Tie", "Computer Won", "You Won"]
winText = valText(length//2, 550, "Result Here")


while running:

    if not gameOver and firstTurn and not isPlayWhite or not firstTurn and isPlayWhite:
        print("Playing")
        if remPieces == board.size**2:
            resp = (random.randint(0, remPieces-1), 0)
        else:
            resp = minimaxAB(board.convertToString(), 0,
                             remPieces, firstTurn, AlphaBeta=menuResult[0], Heuristic=menuResult[1])
        print(resp)
        remPieces = remPieces - 1
        board.placeObject(
            (resp[0] % board.size, resp[0]//board.size), firstTurn)
        print("Played")
        firstTurn = not firstTurn
        print(board.convertToString(), getStateValue(board.convertToString()))
        check = isTerminal(board.convertToString())
        if check[0]:
            print(winName[check[1]])
            winText.updateContent(winName[check[1]])
            gameOver = True
            print("Game Over")

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
            sel = board.getClicked(pygame.mouse.get_pos())
            if sel != None:
                # print(sel.index)
                remPieces = remPieces - 1
                board.placeObject(
                    (sel.index % board.size, sel.index//board.size), isPlayWhite)
                firstTurn = not firstTurn
                print(board.convertToString(),
                      getStateValue(board.convertToString()))
                check = isTerminal(board.convertToString())
                if check[0]:
                    gameOver = True
                    print(winName[check[1]])
                    winText.updateContent(winName[check[1]])
                    print("Game Over")

    Draw()
