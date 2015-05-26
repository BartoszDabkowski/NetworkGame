__author__ = 'Bartosz'

from Tkinter import *
import time
import tkMessageBox
from socket import *
import select

class U3T_Game:

    def __init__(self, r, createOrJoin, host, port, primaryServerHost, primaryServerPort, gameID):
        self.r = r
        self.canvas = Canvas(r, width=700, height=700)
        self.createOrJoin = createOrJoin
        self.gameOn = False
        self.host = host
        self.port = port
        self.primaryServerHost = primaryServerHost
        self.primaryServerPort = primaryServerPort
        self.gameID = gameID
        self.gameCells = ['~' for x in range(9)]
        self.scButtons = [[[Label, 0, 0] for x in range(9)] for y in range(9)]
        self.singleCells = [['~' for x in range(9)] for y in range(9)]
        self.initializeGame()
        self.testCoord = []

#====================================================================================================

    def initializeGame(self):
        # if you create you become the 'server'
        if(self.createOrJoin == 'create'):
            # waiting for player
            waitingLabel = Label(self.r, text=('Game ' + self.gameID + ': Waiting for player...'), font='Georgia 36', pady=10)
            cancelButton = Button(self.r, text='Cancel', command=lambda: self.cancelCreate())
            waitingLabel.pack()
            cancelButton.pack()
            self.r.update()

            self.player = 'O'

            print('waiting')

            # become a server and wait for a connection
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.bind(('', self.port))
            self.sock.listen(5)

            self.s, addr = self.sock.accept()
            self.s.setblocking(0)
            print('server: connected')

            waitingLabel.destroy()

            self.gameOn = True

        # if you join then you will connect to a 'server'
        else:
            self.player = 'X'

            self.s = socket(AF_INET, SOCK_STREAM)
            self.s.connect((self.host, self.port))
            self.s.setblocking(0)
            print('client: connected')

            self.gameOn = True

        # draw the board
        self.canvas.pack()
        self.drawGameBoard()
        self.r.update()

        img = PhotoImage(master=self.canvas, file="imageXO.gif", width=55, height=55)
        bigCells = [50, 250, 450]
        smallCells = [0, (200 / 3) + 4, (200 / 3) * 2 + 4]

        gcLoc = 0
        scLoc = 0

        # Initialize single cells and place single cell buttons
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        self.scButtons[gcLoc][scLoc] = [Label(self.canvas, image=img, bg="white"),
                                                        bigCells[j] + smallCells[l] + 2,
                                                        bigCells[i] + smallCells[k] + 2]
                        self.scButtons[gcLoc][scLoc][0].place(x=bigCells[j] + smallCells[l] + 2,
                                                              y=bigCells[i] + smallCells[k] + 2)

                        self.scButtons[gcLoc][scLoc][0].bind("<Button>",
                            lambda event, coord=[gcLoc, scLoc]: self.activateButton(event, coord))
                        scLoc += 1
                gcLoc += 1
                scLoc = 0
        gcLoc = 0

        forfeitButton = Button(self.canvas,text='Forfeit', command=self.drawEndGameMessage('O'))
        forfeitButton.place(x=325, y=675)

        # create player is second to go. First freeze everything and receive first cord.
        # join players whole board lights up
        if(self.createOrJoin == 'create'):
            self.freezeCells('!')
            coordinates = self.receiveMove()
            print(coordinates[0], coordinates[1])
            self.receiveCoord(coordinates)
        else:
            self.highlightGameBoard(True)


#====================================================================================================

    def drawGameBoard(self):
        buf = 700 / 14
        x1 = 700 - buf
        x2 = (700 - 2 * buf) / 3 + buf
        x3 = 2 * (700 - 2 * buf) / 3 + buf

        #Draw big game board
        self.canvas.create_rectangle(buf, buf, x1, x1, width=4)
        self.canvas.create_line(buf, x2, x1, x2, width=4)
        self.canvas.create_line(buf, x3, x1, x3, width=4)
        self.canvas.create_line(x2, buf, x2, x1, width=4)
        self.canvas.create_line(x3, buf, x3, x1, width=4)

        buf = (200 / 3)
        coordinates = [50 + buf + 1, 50 + buf * 2 + 1, 50 + buf * 4 + 3,
                       50 + buf * 5 + 3, 50 + buf * 7 + 5, 50 + buf * 8 + 5]

        # Draw small game cells
        # Draw vertical lines
        for i in range(6):
            self.canvas.create_line(coordinates[i], 50, coordinates[i], 650, width=2)

        # Draw horizontal lines
        for i in range(6):
            self.canvas.create_line(50, coordinates[i], 650, coordinates[i], width=2)

#====================================================================================================
    # All game logic in activateButton
    def activateButton(self, event, coord):
        gcLoc = coord[0]
        scLoc = coord[1]

        if self.gameCells[gcLoc] == '~':
            self.scButtons[gcLoc][scLoc][0].destroy()
            self.singleCells[gcLoc][scLoc] = self.player
            self.drawScShape(self.player, coord)
            self.determineGameCellWinner(gcLoc)
            self.freezeCells(scLoc)                    #Uncomment this and comment NETWORKING to fix
            self.determineWinner()
            self.printStats()
            self.r.update()
            self.sendMove(gcLoc, scLoc)                 # Socket send code
            # send message

            #------NETWORKING------#
            ####################################
            self.freezeCells('!') #'!' for NETWORKING
            coordinates = []
            coordinates = self.receiveMove()            # Socket receive code
            print(coordinates[0], coordinates[1])
            self.receiveCoord(coordinates)
            ####################################

#====================================================================================================
    #______NETWORKING_______
    def receiveCoord(self, coord):
        gcLoc = coord[0]
        scLoc = coord[1]

        print(gcLoc, scLoc)
        self.scButtons[gcLoc][scLoc][0].destroy()
        self.singleCells[gcLoc][scLoc] = self.player
        self.drawScShape(self.player, coord)
        self.determineGameCellWinner(gcLoc)
        self.freezeCells(scLoc)
        self.determineWinner()
        self.printStats()

#====================================================================================================

    def drawGcShape(self, shape, gcLoc):
        coord = [50, 250, 450]
        scLocs = []

        self.gameCells[gcLoc] = shape

        # Append coordinates for each single cell in the game cell
        for i in range(3):
            for j in range(3):
                scLocs.append([coord[j], coord[i]])

        x = scLocs[gcLoc][0]
        y = scLocs[gcLoc][1]
        s = 200
        b = 200 / 10
        s = 700 / 14

        self.canvas.create_rectangle(x, y, x + 200, y + 200, fill="white", outline="black", width=4)

        # Destroy all buttons in game cell
        for i in range(9):
            if self.singleCells[gcLoc][i] != 'X' or self.singleCells[gcLoc][i] != 'O':
                self.scButtons[gcLoc][i][0].destroy()

        # Place shape in game cell
        if shape == 'O':
            self.canvas.create_oval(x + b, y + b, x + 200 - b, y + 200 - b, outline="red", width=12)
        else:
            self.canvas.create_line(x + b, y + b, x + 200 - b, y + 200 - b, fill="blue", width=12)
            self.canvas.create_line(x + b, y + 200 - b, x + 200 - b, y + b, fill="blue", width=12)

#====================================================================================================

    def drawScShape(self, shape, coord):
        buf = 200 / 20
        s = -4

        x = self.scButtons[coord[0]][coord[1]][1]
        y = self.scButtons[coord[0]][coord[1]][2]

        # Place shape in single cell
        if shape == 'O':
            self.canvas.create_oval(x + buf + s + 2, y + buf + s + 2,
                                    x + 60 - buf - s, y + 60 - buf - s, outline="red", width=7)
            self.player = 'X'
        elif shape == 'X':
            self.canvas.create_line(x + buf - 2, y + buf - 2, x + 60 + s, y + 60 + s,
                                    fill="blue", width=7)
            self.canvas.create_line(x + buf - 2, y + 60 + s, x + 60 + s, y + buf - 2,
                                    fill="blue", width=7)
            self.player = 'O'

#====================================================================================================

    def freezeCells(self, noFreeze):
        ####################################
        if(noFreeze == '!'):
            for i in range(9):
                if self.gameCells[i] == '~':
                    self.gameCells[i] = '@'
                self.highlightCellSection(False, i)
            return
        ####################################


        # Normalize Cells
        for i in range(9):
            if self.gameCells[i] == '@':
                self.gameCells[i] = '~'
            self.highlightCellSection(False, i)

        # Freeze all cells but target cell
        # if target cell is free
        if self.gameCells[noFreeze] == '~':
            for i in range(9):
                if self.gameCells[i] == '~':
                    self.gameCells[i] = '@'
            self.gameCells[noFreeze] = '~'
            self.highlightCellSection(True, noFreeze)
            return

        self.highlightGameBoard(True)

#====================================================================================================

    def highlightGameBoard(self, boolean):
        if(boolean == True):
            self.canvas.create_rectangle(50, 50, 650, 650, outline="#00CC00", width=4)
        else:
            self.canvas.create_rectangle(50, 50, 650, 650, outline="black", width=4)

#====================================================================================================

    def highlightCellSection(self, boolean, gcLoc):
        coord = [50, 250, 450]
        gcLocs = []

        for i in range(3):
            for j in range(3):
                gcLocs.append([coord[j], coord[i]])

        x = gcLocs[gcLoc][0]
        y = gcLocs[gcLoc][1]
        s = 200

        if boolean == True:
            self.canvas.create_rectangle(x, y, x + s, y + s, outline="#00CC00", width=4)
        else:
            self.canvas.create_rectangle(x, y, x + s, y + s, outline="black", width=4)

#====================================================================================================

    def determineGameCellWinner(self, gcLoc):
        player = 'X'

        # Check each player victory status for game cell
        for i in range(2):
            # Horizontal victory
            for j in range(0, 7, 3):
                if(self.singleCells[gcLoc][j] == player and
                   self.singleCells[gcLoc][j + 1] == player and
                   self.singleCells[gcLoc][j + 2] == player):
                    self.drawGcShape(player, gcLoc)
                    return True

            # Vertical victory
            for j in range(0, 3):
                if(self.singleCells[gcLoc][j] == player and
                   self.singleCells[gcLoc][j + 3] == player and
                   self.singleCells[gcLoc][j + 6] == player):
                    self.drawGcShape(player, gcLoc)
                    return True

            # Diagonal victory
            for j in range(0, 3, 2):
                if(self.singleCells[gcLoc][j] == player and
                   self.singleCells[gcLoc][4] == player and
                   self.singleCells[gcLoc][8 - j] == player):
                    self.drawGcShape(player, gcLoc)
                    return True

            # Switch player
            player = 'O'

        noWinner = 0
        for i in range(9):
            if self.singleCells[gcLoc][i] != '~':
                noWinner += 1

        if noWinner == 9:
            self.gameCells[gcLoc] = '!'

        return False

#====================================================================================================

    def determineWinner(self):
        player = 'X'

        victory = 0

        # Check each player victory status for game
        for i in range(2):
            # Horizontal victory
            for j in range(0, 7, 3):
                if(self.gameCells[j] == player and
                   self.gameCells[j + 1] == player and
                   self.gameCells[j + 2] == player):
                    self.endGame()
                    self.drawVictory(victory)
                    self.drawEndGameMessage(player)
                    return True
                victory += 1

            # vertical victory
            for j in range(0, 3):
                if(self.gameCells[j] == player and
                   self.gameCells[j + 3] == player and
                   self.gameCells[j + 6] == player):
                    self.endGame()
                    self.drawVictory(victory)
                    self.drawEndGameMessage(player)
                    return True
                victory += 1

            # Diagonal victory
            for j in range(0, 3, 2):
                if(self.gameCells[j] == player and
                   self.gameCells[4] == player and
                   self.gameCells[8 - j] == player):
                    self.endGame()
                    self.drawVictory(victory)
                    self.drawEndGameMessage(player)
                    return True
                victory += 1

            # Switch player and reset victory number
            player = 'O'
            victory = 0

        noWinner = 0
        for i in range(9):
            if self.gameCells[i] != '~':
                noWinner += 1

        if noWinner == 9:
            self.drawEndGameMessage('!')
            return True
        return False

#====================================================================================================

    def endGame(self):
        for i in range(9):
            self.highlightCellSection(False, i)
            for j in range(9):
                if self.singleCells[i][j] == '~':
                    self.scButtons[i][j][0].destroy()

#====================================================================================================

    def drawEndGameMessage(self, player):
        if player == 'X':
            win = PhotoImage(file="youWin.gif")
            l = Label(self.canvas, image=win)
            l.image = win
            if (self.createOrJoin == 'create'):
                self.sendGameResult(1)

        elif player == 'O':
            lose = PhotoImage(file="youLose.gif")
            l = Label(self.canvas, image=lose)
            l.image = lose
            if (self.createOrJoin == 'create'):
                self.sendGameResult(0)
        else:
            draw = PhotoImage(file="Draw.gif")
            l = Label(self.canvas, image=draw)
            l.image = draw

        b = Button(self.canvas, text='Exit', command=self.r.destroy)

        l.place(x=200, y=270)
        b.place(x=320, y=375)

#====================================================================================================

    def sendGameResult(self, result):

        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.primaryServerHost, self.primaryServerPort))
        gameResult = 'end_' + self.gameID + " " + result
        s.send(gameResult)
        s.close()

#====================================================================================================

    def drawVictory(self, victory):
        # Accross top
        if(victory == 0):
            self.canvas.create_line(60, 150, 640, 150, width=15)
        # Across middle
        elif(victory == 1):
            self.canvas.create_line(60, 350, 640, 350, width=15)
        # Across bottom
        elif(victory == 2):
            self.canvas.create_line(60, 550, 640, 550, width=15)
        # Down the left
        elif(victory == 3):
            self.canvas.create_line(150, 60, 150, 640, width=15)
        # Down the middle
        elif(victory == 4):
            self.canvas.create_line(350, 60, 350, 640, width=15)
        # Down the right
        elif(victory == 5):
            self.canvas.create_line(550, 60, 550, 640, width=15)
        # Diagonal right to left
        elif(victory == 6):
            self.canvas.create_line(60, 60, 640, 640, width=15)
        # Diagonal left to right
        elif(victory == 7):
            self.canvas.create_line(60, 640, 640, 60, width=15)

#====================================================================================================
    #DEBUGGING ONLY
    def printStats(self):

        scLoc = 0
        gcLoc = 0
        gcCheck = 0

        print("Single Cells:")
        for i in range(3):
            print('+-----------------------+')
            for j in range(3):
                for k in range(3):
                    print("|"),
                    print(self.singleCells[gcLoc][scLoc], self.singleCells[gcLoc][scLoc + 1],\
                        self.singleCells[gcLoc][scLoc + 2],)
                    gcLoc += 1
                    if j == 2:
                        gcCheck += 1
                scLoc += 3
                gcLoc = gcCheck
                print("|")
            scLoc = 0
        print('+-----------------------+')

        count = 0
        print("Game Cells:")
        print("+-------+")
        for i in range(3):
            print("|"),
            for j in range(3):
                print(self.gameCells[count]),
                count += 1
            print('|')
        print("+-------+")
        print('*==============================*')

    def gameOn(self):
        return self.gameOn

    def sendMove(self, gcLoc, scLoc):
        msg = str(gcLoc) + " " + str(scLoc)
        self.s.send(msg)

    def receiveMove(self):
        while 1:
            ready = select.select([self.s], [], [])
            if ready[0]:
                msg = self.s.recv(1024)
                msg = msg.split()
                coordinates = [int(msg[0]), int(msg[1])]
                return coordinates

    # cancel creating a new game
    def cancelCreate(self):
        self.sock.close()
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.primaryServerHost, self.primaryServerPort))
        s.send('cancel')
        self.r.destroy()
        print('Cancelled create')