# CSS432 - Client
# Bethel Heo, Bartosz Dabkowski, Xiiaoyu Liang
#
# Client.py
# Program for the game, connection to server, and P2P connection

from U3T_Game import *

class Client(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master    = master
        self.primaryServerPort = 12000
        self.primaryServerHost = 'uw1-320-14.uwb.edu'

        # create main frame
        mainFrame = Frame(master, width=700, height=700)
        mainFrame.pack()

        # create title label from image
        titlePhoto = PhotoImage(file='title.gif')
        titleLabel = Label(mainFrame, image=titlePhoto)
        titleLabel.image = titlePhoto
        titleLabel.pack()

        # create top score button
        topPhoto = PhotoImage(file='top.gif')
        topButton = Button(mainFrame, image=topPhoto, command=lambda: self.top())
        topButton.image = topPhoto
        topButton.pack()

        # create join button
        joinPhoto = PhotoImage(file='join.gif')
        joinButton = Button(mainFrame, image=joinPhoto, command=lambda: self.join())
        joinButton.image = joinPhoto
        joinButton.pack()

        # create create button
        createPhoto = PhotoImage(file='create.gif')
        createButton = Button(mainFrame, image=createPhoto, command=lambda: self.create())
        createButton.image = createPhoto
        createButton.pack()

        # create exit button
        exitPhoto = PhotoImage(file='exit.gif')
        exitButton = Button(mainFrame, image=exitPhoto, command=lambda: self.close(self.master))
        exitButton.image = exitPhoto
        exitButton.pack()

    # top score
    def top(self):
        topWindow = Toplevel()
        topWindow.title('Top Scores')

        topLabel = Label(topWindow, text='Top Scores', font='Georgia 36')
        topLabel2 = Label(topWindow, text='Ordered by number of wins')
        topTitle = Label(topWindow, text='IP Address'.ljust(20) + 'Wins'.rjust(5))
        topLabel.pack()
        topLabel2.pack()
        topTitle.pack()

        # connect to primary server and ask for top score list
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.primaryServerHost, self.primaryServerPort))
        s.send('top')
        topList = s.recv(4096)
        topList.split()
        s.close()

        # for testing
        #topList = ['123.123.123', '1', '123.123.123', '2', '123.123.123', '3']

        ip = 0
        wins = 1
        # check length of list. Only do top 10 or less
        if(topList == 'empty'):
            scoreLabel = Label(topWindow, text='[No scores yet]')
            scoreLabel.pack()
        else:
            if(len(topList) < 10):
                x = len(topList)
            else:
                x = 10
            for score in range(0, x):
                scoreText = (topList[ip].ljust(20) + topList[wins].rjust(5))
                scoreLabel = Label(topWindow, text=scoreText)
                scoreLabel.pack()
                ip += 2
                wins += 2

        # close window
        closeButton = Button(topWindow, text='Close', command=lambda: self.close(topWindow))
        closeButton.pack()

    # join game
    def join(self):
        joinWindow = Toplevel()
        joinWindow.title('Select a game to join')

        scrollbar = Scrollbar(joinWindow, orient=VERTICAL)
        listbox = Listbox(joinWindow, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox.pack(side=LEFT, fill=BOTH, expand=1)

        # connect to primary server and ask for game list
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.primaryServerHost, self.primaryServerPort))
        s.send('list')
        msg = s.recv(4096)
        msg.split()
        s.close()

        # creates a selectable list of games
        for game in msg:
            game = 'Game ' + game
            listbox.insert(END, game)

        # join selected game
        joinButton = Button(joinWindow, text='Join', command=lambda: self.joinGame(listbox.get(listbox.curselection()), joinWindow))
        joinButton.pack()

        # close window
        closeButton = Button(joinWindow, text='Close', command=lambda: self.close(joinWindow))
        closeButton.pack()

    # join selected game
    def joinGame(self, selectedGame, joinWindow):
        # connect to primary server and send the game ID
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.primaryServerHost, self.primaryServerPort))
        # parse Game x to just x
        selectedGame = selectedGame[5:]
        print(selectedGame)

        joinSelectedGame = 'join_' + selectedGame
        s.send(joinSelectedGame)
        # receive the host and port from primary server
        msg = s.recv(4096)

        print(msg)

        first = msg.find('\'')
        msg = msg[first + 1:]

        ip = msg[:msg.find('\'')]
        port = msg[msg.find(' ') + 1 : msg.find(')')]

        print ('connecting to: ', ip, port)

        # close the join window
        joinWindow.destroy()

        # new window for game
        gameWindow = Toplevel()
        gameWindow.geometry('+500+400')
        game = U3T_Game(gameWindow, 'join', ip, int(port), self.primaryServerHost, self.primaryServerPort)

    # start a new game
    def create(self):
        # send primary server ip address and port number
        print('connecting to primary server')
        s = socket(AF_INET, SOCK_STREAM)
        print('socket created')
        s.connect((self.primaryServerHost, self.primaryServerPort))
        print('sending ip and port')
        s.send('create')

        # receive game ID from primary server
        gameIDandPort = s.recv(1024)
        print('Game ID and port = ' + gameIDandPort)
        s.close()

        host = ''
        port = gameIDandPort[gameIDandPort.find('_') + 1:]
        gameID = gameIDandPort[:gameIDandPort.find('_')]

        # new window for game
        gameWindow = Toplevel()
        gameWindow.geometry('+500+400')
        gameWindow.title('You are in game: ' + gameID)

        game = U3T_Game(gameWindow, 'create', host, int(port), self.primaryServerHost, self.primaryServerPort)

    # exit/close window
    def close(self, frame):
        frame.destroy()

# Executable section.
if __name__ == '__main__':

    root = Tk()
    root.title('U3T')

    client = Client(root)

    root.mainloop()

