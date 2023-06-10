"""
Name: Jin Rong Song
AndrewID: jinrongs

Project: 112 Joyride
"""


from cmu_112_graphics import *
import random
import tkinter as tk

"""
Printing 2d list code from 15112 course notes. Used to debug.
https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
"""
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

def print2dList(L):
    print(repr2dList(L))

"""
Round half up code from previous homeworks in the course
"""
import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


class playerClass(object):     #class for player, contains position, hitbox,
                                #gravity, movement, powerups on etc.
    def __init__(self):
        self.x = -150
        self.y = 680
        self.isMoving = False
        self.gravityFall = 2
        self.radX = 25
        self.radY = 30
        self.invincible = False
        self.coins = 0
    
    def movePlayer(self):               #moving the player up
        self.isMoving = True
        self.y -= 20
        if self.y <= 30:
            self.y = 30
        self.isMoving = False
        self.gravityFall = 0
    
    def collision(self,other):  #testing player collisions
        otherX = set([i for i in range(other.startX -other.radX,
                                            other.startX +other.radX)])
        otherY = set([j for j in range(other.startY-other.radY,
                                             other.startY+other.radY)])
        for x in range(self.x - self.radX, self.x + self.radX):
            for y in range(self.y - self.radY, self.y + self.radY):
                if (x in otherX) and (y in otherY):
                    return True

class missile(object):   
            #class for missiles, containing x,y coordinates and hitboxes
    def __init__(self):
        self.startX = 1400
        self.missileLaunched = False
        self.startY = None
        self.radX = 30
        self.radY = 30
    
    def getY(self,other):   #gets the players position for tracking
        self.startY = other.y
    
    def shooting(self):   #keeps the missile moving forward
        self.startX = self.startX - 35
        if self.startX <= 0:
            self.missileLaunched = False
            self.startX = 1400

class powerUp():  #class for powerups, containing x,y coordinates and hitboxes
    def __init__(self):
        self.x = None
        self.y = None
        self.radX = 30
        self.radY = 30
        self.collected = False

class shield(powerUp):  #superclass for shields, checks for collisions
    def shieldOn(self,other):
        otherX = set([i for i in range(other.x -other.radX,
                                            other.x +other.radX)])
        otherY = set([j for j in range(other.y-other.radY,
                                             other.y+other.radY)])
        for i in range(60):
            if (self.y + self.radY - i) in otherY and \
                    (self.x-self.radX +i) in otherX:
                other.invincible = 1  #makes the player invincible
                self.collected = True #indicates that powerup has been collected

class boost(powerUp):  #superclass for boosts, checks for collisions
    def boostOn(self,other):
        otherX = set([i for i in range(other.x -other.radX,
                                            other.x +other.radX)])
        otherY = set([j for j in range(other.y-other.radY,
                                             other.y+other.radY)])
        for i in range(70):
            if (self.y + self.radY - i) in otherY and \
                    (self.x-self.radX +i) in otherX:
                other.invincible = 1 #makes the player invincible
                self.collected = True

class zap:   #class for zappers, contains locations, hitboxes
    def __init__(self):
        self.x = None
        self.y = None
        self.radX = 70
        self.radY = 70
        self.row = None
        self.col = None

    def collisionZapper(self,other):  #checks for collisions
        otherX = set([i for i in range(other.x -other.radX,
                                            other.x +other.radX)])
        otherY = set([j for j in range(other.y-other.radY,
                                             other.y+other.radY)])
        for i in range(140):
            if (self.y + self.radY - i) in otherY and \
                    (self.x-self.radX +i) in otherX:
                return True

class otherZap(zap):  #superclass for zapper in the other direction
    def collisionOther(self,other):
        otherX = set([i for i in range(other.x-other.radX,
                                            other.x +other.radX)])
        otherY = set([j for j in range(other.y-other.radY,
                                             other.y+other.radY)])
        for i in range(140):
            if (self.y - self.radY + i) in otherY and \
                    (self.x - self.radX +i) in otherX:
                return True

class coins:  #coins, checks for collisions, and sees if they are collected
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.x =  col*70 + 35 +1400
        self.y =  row*70 + 35
        self.radX = 20
        self.radY = 20
        self.collected = False
    
    def collection(self,other):
        otherX = set([i for i in range(other.x -other.radX,
                                            other.x +other.radX)])
        otherY = set([j for j in range(other.y-other.radY,
                                             other.y+other.radY)])
        for i in range(40):
            if (self.y + self.radY - i) in otherY and \
                    (self.x-self.radX +i) in otherX:
                self.collected = True
                other.coins += 1
                return True


def appStarted(app):  #contains variables
    getLeaderboard(app)  #retrieves leaderboard from file
    app.message = "Click to enter your username!"
    app.username = "player"
    app.player = playerClass()  #starts the player
    app.gameStart = False
    app.score = 0  #keeps score
    app.timer = 1
    app.count = 0  #keeps track of when things are firing
    app.gameOver = False
    app.missileLaunch = 50  #keeps track of when missiles are firing
    app.instructions = False  #whether or not instructions have been clicked
    app.showLeaderboard = False  #shows leaderboard
    app.distanceMove = 30  #set movement distance
    playerSprites(app)  #loads sprits for obstacles, coins, pwerups, and player
    background(app)
    coin(app)
    firingMissile(app)
    zapper(app)
    app.missile = missile()
    powerup(app)
    grid(app)   #creates grid to generate everything
    app.tracking = -2  #how long missiles track far
    app.numbZap = 3  #number of zappers in each map generated
    app.zapperLocation = []  #keeps track of zapper locations
    placeZapper(app)  #places zappers
    app.coins = []  #keeps track of coin locations
    app.boardGenerated = 0  #how long the player has gone for
    app.coinPath = []    #keeps track of coin pattern and positions 
    app.coinPosition = []
    placeCoins(app)   #place coins
    app.powerup = None  #checks if powerup is on
    app.numbPowerups = 0  
    placePowerups(app)   #places powerups 
    app.reset = 2800     #when to reset the grid
    app.playerPositionGrid = 0
    app.hint=[]   #keeps track of hint path
    app.hintPath = []
    app.solveable = None   #checks if solveable map or not
    isBoardLegal(app)      #checks if board is legal using is solvable
    app.showHint = False   #shows hint
    app.powerupTimer = None  #how long powerup has been on for
    app.usernameAdded = False #name added to leaderboard
"""
Inspired by Spritesheet and images note sections in 15112 course website
Sprites from "https://jetpackjoyride.fandom.com/wiki/Barry_Steakfries/Gallery"
"""
def playerSprites(app):  #loads player sprites for running, jumping etc.
    app.spriteCounter = 0
    app.spritesRunning = []
    app.spritesFlying = []
    app.playerSprites = app.loadImage("Sprites.png")
    app.playerSprites = app.scaleImage(app.playerSprites,0.5)
    app.num = 4
    for i in range(app.num):
        sprite = app.playerSprites.crop((35+70*i,20, 105+70*i, 95))
        app.spritesRunning.append(sprite)
    for i in range(app.num):
        sprite = app.playerSprites.crop((35+70*i,95, 105+70*i, 160))
        app.spritesFlying.append(sprite)
    app.spriteCounter = 0

"""
Image from https://twitter.com/danilojunior_fc/status/37158389172890009
"""
def background(app):  #loads background
    app.background = app.loadImage("background.png")
    app.background = app.background.crop((300,0, 650, 450))
    app.background = app.scaleImage(app.background, 2)
    app.backgroundCoord = [[0,400],[600,400],[1200,400],[1800,400]]

"""
Images of powerups from https://jetpackjoyride.fandom.com/wiki/Power-Ups
"""
def powerup(app):  #loads powerups
    app.boost = app.loadImage("boost.png")
    app.boost = app.scaleImage(app.boost, 0.3)

    app.shield = app.loadImage("shield.png")
    app.shield = app.scaleImage(app.shield, 0.3)

"""
Coin image from https://www.pngwing.com/en/free-png-nvjxc
"""
def coin(app):  #loads coins
    app.coin = app.loadImage("coin.png")
    app.coin = app.scaleImage(app.coin, 0.1)

"""
Missile images from https://jetpackjoyride.fandom.com/wiki/Missile
"""
def firingMissile(app):  #loads missiles and warning symbols
    app.missiles = app.loadImage("Missile.png")
    app.missiles = app.scaleImage(app.missiles, 2)

    app.missileIcon = app.loadImage("Missile_Target.png")
    app.missileIcon = app.scaleImage(app.missileIcon, 1)

    app.missileShoot = app.loadImage("missileAlarm.png")
    app.missileShoot = app.scaleImage(app.missileShoot, 1)


"""
Zapper images from https://jetpackjoyride.fandom.com/wiki/Zapper
"""
def zapper(app):   #loads zappers
    app.zapper = app.loadImage("Laser.png")
    app.zapper = app.scaleImage(app.zapper, 1)
    app.zapperOther = app.loadImage("LaserOther.png")
    app.zapperOther = app.scaleImage(app.zapperOther, 1)


def mousePressed(app,event):
    #mouse pressed for instructions and leaderboard
    app.instructions = False
    app.showLeaderboard = False
    if app.gameStart != True and app.instructions == False and \
        app.showLeaderboard == False:
        if 200<= event.x <=600 and 600 <= event.y <=700:
            app.instructions = True
        if 800<= event.x <=1200 and 600 <= event.y <=700:
            app.showLeaderboard = True

def keyPressed(app,event):
    if (event.key == "Enter") and app.username !=None: #starts the game
        app.gameStart = True
    elif (event.key == "Up") and app.player.x == 300: #moves player up
        app.player.movePlayer()
    elif (event.key == "h"):  #shows hint
        app.showHint = True
    if (event.key == "Space"):      #resets the game
        appStarted(app)

def keyReleased(app, event):
    if (event.key == "Up"):
        app.player.movePlayer()

def timerFired(app):
    if app.gameStart == True:
        app.count += app.timer
        if app.player.x != 300:
            app.player.x += 30   #running into the screen
        if app.player.invincible == False:  #checks for collisions with zapper
            for i in range(len(app.zapperLocation)):
                if isinstance(app.zapperLocation[i],otherZap)!=True:
                    if app.zapperLocation[i].collisionZapper(app.player)== True:
                        app.gameOver= True
                else:
                    if app.zapperLocation[i].collisionOther(app.player)==True:
                        app.gameOver= True
        
        for i in range(len(app.coinPosition)):  #checks collision for coins
            if app.coinPosition[i].collection(app.player):
                app.player.coins += 1
                app.score += 100
    
    if app.gameStart==True and app.player.x == 300 and app.gameOver !=True:
        if app.powerup != None:
            app.powerup.x -= 30
            if isinstance(app.powerup,shield):  #checks if player got powerup
                app.powerup.shieldOn(app.player)
            else:
                app.powerup.boostOn(app.player)
            if isinstance(app.powerup,boost) and app.powerup.collected == True:
                app.playerPositionGrid += 30
                app.distanceMove = 60  #boost moves player faster

        if app.player.invincible != False and app.player.invincible <= 20:
            app.player.invincible += 1 
            #keeps track of how long player has powerup
        else:
            app.player.invincible = False
            app.distanceMove = 30

        app.playerPositionGrid += app.distanceMove
        app.reset -= app.distanceMove #reset at certain point
        app.score += 10
        for j in range(len(app.hintPath)):
            app.hintPath[j][0]-= app.distanceMove

        #moves everything together, coins, backgrounds, zappers etc
        if app.backgroundCoord[0][0] <= -600:
            app.backgroundCoord.pop(0)
        if len(app.backgroundCoord)==3:
            app.backgroundCoord.append([1800,400])
        for i in range(len(app.backgroundCoord)):
            app.backgroundCoord[i][0] -= app.distanceMove
        if len(app.zapperLocation) == app.numbZap:
            for i in range(app.numbZap):
                app.zapperLocation[i].x -= app.distanceMove
            if app.reset <= 0:
                reset(app)

        if app.coinPosition != []:
            for i in range(len(app.coinPosition)):
                app.coinPosition[i].x -= app.distanceMove

#looping through sprite animations
    app.spriteCounter = (1 + app.spriteCounter) % 4 

    if app.gameStart == True and app.player.isMoving == False:
        gravity(app)

    #random timer to set off missile, and how long to track
    if  app.count >= app.missileLaunch and \
                app.missile.missileLaunched == False:
        app.missile.getY(app.player)
        app.missile.missileLaunched = True
        app.missileLaunch = app.count + random.randint(50,100)

    elif app.missileLaunch - app.count < 0:
        if app.player.collision(app.missile) == True and \
            app.player.invincible == False:
            app.gameOver= True
        app.missile.shooting()
        app.missile.startX -= app.distanceMove + 5
        if app.missileLaunch - app.count >= app.tracking:
            app.missile.getY(app.player)

    if app.powerupTimer != None:
        app.powerupTimer += 1

    if app.count != 0 and app.tracking >= -10:
        if app.count % 100 == 0:
            app.tracking -= 1
    
    if app.gameOver == True and app.usernameAdded == False:
        updateLeaderboard(app)
        app.usernameAdded == True

def reset(app): #resets everything
    if app.boardGenerated % 3 == 0:
        app.numbZap += 1
    grid(app)
    app.zapperLocation = []
    placeZapper(app)
    app.coinPath = []
    placeCoins(app)
    app.reset = 2800
    app.solveable = None
    app.showHint = False
    app.hintPath = []
    app.boardGenerated += 1
    app.hint = []
    app.playerPositionGrid = 0
    app.numbPowerups = 0
    app.powerup = None
    placePowerups(app)
    isBoardLegal(app)


#app.missile = missile(app.player.y)

def gravity(app): #gravity for player
    if app.player.isMoving != True:
        if app.player.y < 680:
            app.player.y += app.player.gravityFall
            app.player.gravityFall += 5
    if app.player.y > 680:
        app.player.y = 680

def startScreen(app,canvas): #prints the starting screen
    canvas.create_text(app.width/2, app.height/2, fill="red",
                           text="Welcome to 112 Joyride!", 
                                    font='Arial 50 bold')
    if app.count %2 == 0: #blinking start
        canvas.create_text(app.width/2,app.height/2 + 100, fill="black", 
                        text = "Press Enter to Start",
                                    font='Arial 32 bold')

def drawGameOver(app,canvas): #draws game over
    canvas.create_text(app.width/2, app.height/2, fill="red",
                           text="GAME OVER", 
                                    font='Arial 100 bold')
    canvas.create_text(app.width/2,app.height/2 + 100, fill="black", 
                        text = "Press Space to Restart",
                                    font='Arial 32 bold')

def drawScore(app,canvas):  #prints the score
    canvas.create_text(app.width/2, 50, fill = "black",
                           text="Score: " + str(app.score) ,
                            font=f'Arial 20 bold')

def drawBackground(app,canvas): #draws moving background
    for i in range(4):
        canvas.create_image(app.backgroundCoord[i][0],app.backgroundCoord[i][1], 
                        image=ImageTk.PhotoImage(app.background))

def drawHoningMissile(app,canvas): 
    #draws warnings and missiles at certain time intervals
    if app.missileLaunch  - app.count <=50 and \
                        app.missile.missileLaunched == True:
        canvas.create_rectangle(app.missile.startX-app.missile.radX, app.missile.startY-app.missile.radY,
                                    app.missile.startX+app.missile.radX,
                                    app.missile.startY+app.missile.radY)   
        if app.missileLaunch - app.count <= 0:
            canvas.create_image(app.missile.startX ,app.missile.startY, 
                            image=ImageTk.PhotoImage(app.missiles))
        elif app.missileLaunch - app.count <= 10:
            canvas.create_image(1400, app.player.y, 
                                image=ImageTk.PhotoImage(app.missileShoot))
        elif app.missileLaunch - app.count <= 50 and \
                    (app.missileLaunch - app.count)%10 <= 5:
            canvas.create_image(1400, app.player.y,
                                image=ImageTk.PhotoImage(app.missileIcon))
        
def running(app,canvas): #running sprite
    sprite = app.spritesRunning[app.spriteCounter]
    canvas.create_image(app.player.x, app.player.y, 
            image=ImageTk.PhotoImage(sprite))

def flying(app,canvas): #flying sprite
    sprite = app.spritesFlying[app.spriteCounter]
    canvas.create_image(app.player.x, app.player.y, 
                            image=ImageTk.PhotoImage(sprite))
    
def isLegalPlace(app,row,col,object): #checks if legal place to put anything
    if row < 0 or row >= len(app.grid) or col < 0 or col >= len(app.grid[0]):
        return False
    if app.grid[row][col] != 0:
        return False 
    if row - 1 < 0 and col + 1 < len(app.grid[0]):
        if (app.grid[row][col+1] != 0 and app.grid[row+1][col] != 0):
            return False
    if row + 1 >= len(app.grid) and col + 1 < len(app.grid[0]):
        if (app.grid[row][col+1] != 0 and app.grid[row-1][col] != 0):
            return False
    if 1 <= row <= len(app.grid)-2 and 0<=col + 1 <=len(app.grid[0])-2:
        if (app.grid[row][col+1] != 0 and app.grid[row-1][col] != 0) or \
            (app.grid[row][col+1] != 0 and app.grid[row+1][col] != 0):
            return False
    if isinstance(object,otherZap):
        if app.grid[row+1][col-1] != 0 or app.grid[row-1][col+1] != 0:
            return False
    if isinstance(object,zap):
        if app.grid[row+1][col-1] != 0 or app.grid[row-1][col+1] != 0:
            return False
    return True

def placeZapper(app): #places zappers randomly
    random.seed(random.randint(0,15000))
    while len(app.zapperLocation) < app.numbZap:
        randomZap = random.randint(0,1)
        if randomZap == 1:
            tempZap = zap()
        else: 
            tempZap = otherZap()
        i = random.randint(1,8)
        j = random.randint(1,18)
        if isLegalPlace(app,i,j,tempZap):
            if randomZap == 1:
                app.grid[i][j] = 1
                app.grid[i+1][j-1] = 1
                app.grid[i-1][j+1] = 1
            else:
                app.grid[i][j] = 1
                app.grid[i-1][j-1] = 1
                app.grid[i+1][j+1] = 1
            tempZap.x = j*70 + 35 +1400
            tempZap.col = j
            tempZap.y = i*(70) +35
            tempZap.row = i
            app.zapperLocation += [tempZap]

def drawZapper(app,canvas): #draws zappers in zapper locations
    if len(app.zapperLocation) == app.numbZap:
        for i in range(len(app.zapperLocation)):
            if isinstance(app.zapperLocation[i],otherZap) == True:
                canvas.create_image(app.zapperLocation[i].x,
                                        app.zapperLocation[i].y,
                                    image=ImageTk.PhotoImage(app.zapperOther))
            else:
                canvas.create_image(app.zapperLocation[i].x,
                                        app.zapperLocation[i].y,
                                    image=ImageTk.PhotoImage(app.zapper))

"""
Backtracking coin placement format taken from 15112 notes, backtracking section
of recursion
https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
"""

def placeCoins(app): 
    #wrapper function to get random length of coin pattern and position
    random.seed(random.randint(0,15000))
    app.totalCoinPattern = random.randint(1,3)
    while len(app.coinPath) < app.totalCoinPattern:
        randLen = random.randint(3,5)
        randStartCol = random.randint(0,19-randLen)
        randStartRow = random.randint(0,9)
        if isLegalPlace(app, randStartRow,randStartCol,coin):
            tempCoinPattern = getCoinPattern(app, randStartRow,
                                            randStartCol, -1 ,randLen, [])
            if tempCoinPattern != None:
                app.coinPath += [tempCoinPattern]
    for i in range(len(app.coinPath)):
        for j in range(len(app.coinPath[i])):
            app.coinPosition += [coins(app.coinPath[i][j][0],
                                        app.coinPath[i][j][1])]

def getCoinPattern(app,row, col, lengthSoFar, totalLength, pattern): 
    #recursively generatives coin pattern using backtracking again
    if lengthSoFar == totalLength:
        return pattern
    else:
        for i in [1,0,-1]:
            if isLegalPlace(app, row, col+i,coin):
                app.grid[row][col] = 2
                pattern = pattern +[(row,col)]
                solution = getCoinPattern(app,row, col+i, lengthSoFar+1, 
                                        totalLength, pattern)
                if (solution != None):
                        return solution
                app.grid[row][col] = 0
        return None

def isLegalAI(app,row,col): 
        #ai avoids abstacles, but still goes through coins and powerups
    if row < 0 or row >= len(app.grid) or col < 0 or col >= len(app.grid[0]):
            return False
    if app.grid[row][col]==1:
        return False
    if row - 1 < 0 and col + 1 < len(app.grid[0]):
        if (app.grid[row][col+1] == 1 and app.grid[row+1][col] == 1):
            return False
    if row + 1 >= len(app.grid) and col + 1 < len(app.grid[0]):
        if (app.grid[row][col+1] == 1 and app.grid[row-1][col] == 1):
            return False
    if 1 <= row <= len(app.grid)-2 and 0<=col + 1 <=len(app.grid[0])-2:
        if (app.grid[row][col+1] == 1 and app.grid[row-1][col] == 1) or \
            (app.grid[row][col+1] == 1 and app.grid[row+1][col] == 1):
            return False
    return True

def aiHintSolver(app,startRow, startCol, endCol, hint):
                 #recursively backtracking to get solution
    if startCol == endCol:
        return hint
    else:
        for i in [0,1,-1]:
            if isLegalAI(app,startRow + i , startCol +1):
                newRow = startRow+i
                newCol = startCol+1
                hint = hint + [(newRow,newCol)]
                solution = aiHintSolver(app,newRow, newCol, endCol, hint)
                if solution != None:
                    return solution
                hint.pop()
        return None 

def aiHint(app): #gets ai hint using backtracking
    playerPositionRow = app.player.y//70
    solution = aiHintSolver(app, playerPositionRow, -1, 19,[])
    if solution != None:
        app.hint = solution
        for i in range(len(app.hint)):
            app.hintPath+= [[1400+app.hint[i][1]*70+35,
                            app.hint[i][0]*70+35]]
        return True
    else:
        return None

def drawAiHint(app,canvas): #draws ai hint
    for i in range(len(app.hintPath)):
        if i != len(app.hintPath)-1:
            canvas.create_line(app.hintPath[i][0],app.hintPath[i][1],
            app.hintPath[i+1][0],app.hintPath[i+1][1],width = 10)

def isBoardLegal(app): #checks if board is playable
    if aiHint(app) == None:
        app.solveable = False
    while app.solveable == False:
        grid(app)
        placeZapper(app)
        placeCoins(app)
        if aiHint(app) != None:
            app.solveable == True

def placePowerups(app): #places the powerups randomly on grip
    random.seed(random.randint(0,15000))
    while app.numbPowerups <= 1:
        powerup = random.randint(0,1)
        randCol = random.randint(0,19)
        randRow = random.randint(0,9)
        if isLegalPlace(app,randRow, randCol, powerup):
            app.numbPowerups += 1
            if powerup == 1:
                app.powerup = shield()
                app.powerup.x = 1400+randCol*70 +35
                app.powerup.y = randRow *70+35
            else:
                app.powerup = boost()
                app.powerup.x = 1400+randCol*70 +35
                app.powerup.y = randRow *70+35
        
def drawPowerup(app,canvas): #draws powerups
    if isinstance(app.powerup, shield):
        canvas.create_image(app.powerup.x, app.powerup.y,
                                    image=ImageTk.PhotoImage(app.shield))
    else:
        canvas.create_image(app.powerup.x, app.powerup.y,
                                    image=ImageTk.PhotoImage(app.boost))

def drawCoin(app,canvas): #draws all coins
    for i in range(len(app.coinPosition)):
        if app.coinPosition[i].collected == False:
            canvas.create_image(app.coinPosition[i].x, app.coinPosition[i].y, 
                            image=ImageTk.PhotoImage(app.coin))

def grid(app):  #creates grid
    app.grid = [[0]* 20 for i in range(10)]

def drawInstructionsButton(app,canvas):  #instructions button
    canvas.create_rectangle(200,600,600,700, fill = "green")
    canvas.create_text(400,650,fill="yellow",
                           text="Instructions", 
                                    font='Arial 30 bold')


def drawLeaderboardButton(app,canvas):  #draws the leaderboard
    canvas.create_rectangle(800,600,1200,700,fill = "green")
    canvas.create_text(1000,650,fill="yellow",
                           text="Leaderboard", 
                                    font='Arial 30 bold')

def drawInstructions(app,canvas):  #draws the instructions for the game
    canvas.create_rectangle(350,50,1150,650,fill="white")
    canvas.create_text(800,350,fill="black",
                           text="Press the up arrow key to jump up"+ 
                                    " and avoid obstacles " + "\n" + 
                                "Press the h key if you ever need a hint" + "\n"
                                "Collect powerups:"+ "\n"
                 "Blue shields grant you invincibility for a short time"+ "\n"
        "Green boosts speeds things up and gives you invincibility as well"+ "\n"
                                "Most importantly, have fun!"+ "\n"+ "\n"
                                "Click anywhere to continue", 
                                    font='Arial 20 bold')


"""
Reading and Writing leaderboard file inspired by 15112 course notes
https://www.cs.cmu.edu/~112/notes/notes-strings.html
"""

def readFile(path):  #reads leaderboard file
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):  #adds to leaderboard file
    with open(path, "wt") as f:
        f.write(contents)

def updateLeaderboard(app): #updates leaderboard with player name
    writeFile("Leaderboard.txt", app.username + " " + str(app.score) + "\n")

def getLeaderboard(app): #gets scores and puts name and score into list
    app.scoreList = []
    leaderboard = readFile("Leaderboard.txt")
    for lines in leaderboard.splitlines():
        tempScore = []
        for scores in lines.split(" "):
            tempScore += [scores]
        app.scoreList += [tempScore]


def drawLeaderboard(app,canvas):  #draws leaderboard
    canvas.create_rectangle(350,50,1150,650,fill="white")
    for i in range(len(app.scoreList)):
        if i<16:
            canvas.create_text(750, 300 +20*i, 
                text= app.scoreList[i][0] + " " + app.scoreList[i][1])

def redrawAll(app,canvas):
    canvas.create_image(500,500,image=ImageTk.PhotoImage(app.missiles))
    drawBackground(app,canvas)
    if app.gameStart == False and app.username != None:
        startScreen(app,canvas)  #start screen on
    if app.gameStart != True and app.username != None:
        drawInstructionsButton(app,canvas)
        drawLeaderboardButton(app,canvas)
        if app.instructions == True:
            drawInstructions(app,canvas)
        if app.showLeaderboard == True:
            drawLeaderboard(app,canvas)
    elif app.gameOver == True:
        drawGameOver(app,canvas) #checks if game over
    if app.gameStart == True and app.username != None:
        if app.gameOver != True:
            if app.showHint == True:
                drawAiHint(app,canvas)
            drawZapper(app,canvas)
            drawHoningMissile(app,canvas)
            if app.player.y >= 680:
                running(app,canvas)
            else:
                flying(app,canvas)  
            drawCoin(app,canvas)
            if app.powerup.collected == False:
                drawPowerup(app,canvas)
            if app.powerup!=None and app.powerup.collected != False:
                if isinstance(app.powerup,shield):
                    canvas.create_rectangle(720,670,780,730,fill = "red")
                    canvas.create_image(750,700,
                    image=ImageTk.PhotoImage(app.shield))  #draws shield
                else:
                    canvas.create_rectangle(720,670,780,730,fill = "red")
                    canvas.create_image(750,700,
                    image=ImageTk.PhotoImage(app.boost)) #draws boost
            drawScore(app,canvas)  #draws score


def playJetpack():
    runApp(width=1500, height=750)

playJetpack()
