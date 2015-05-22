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
        self.primaryServerPort = 1234
        self.primaryServerHost = '123.123.123'

        # create main frame
        mainFrame = Frame(master, width=700, height=700)
        mainFrame.pack()

        # create title label from image
        titlePhoto = PhotoImage(file='title.gif')
        titleLabel = Label(mainFrame, image=titlePhoto)
        titleLabel.image = titlePhoto
        titleLabel.pack()

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
        s.send(bytes('list', 'utf-8'))
        msg = s.recv(4096)
        msg.split()
        s.close()

        # creates a selectable list of games
        for game in msg:
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
        s.send(bytes(selectedGame[0], 'utf-8'))
        # receive the host and port from primary server
        msg = s.recv(1024)
        msg.split()

        # close the join window
        joinWindow.destroy()

        # new window for game
        gameWindow = Toplevel()
        game = U3T_Game(gameWindow, 'join', msg[0], int(msg[1]))

    # start a new game
    def create(self):
        # send primary server ip address and port number
        print('connecting to primary server')
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.primaryServerHost, self.primaryServerPort))
        print('sending ip and port')
        host = socket.gethostname()
        port = 1899
        msg = host + " " + str(port)
        s.send(bytes(msg, 'utf-8'))

        # receive game ID from primary server
        gameID = str(self.s.recv(1024), 'utf-8')
        print('Game ID = ' + gameID)
        s.close()

        # new window for game
        gameWindow = Toplevel()
        gameWindow.title('You are in game: ' + gameID)
        game = U3T_Game(gameWindow, 'create', host, port)

    # exit/close window
    def close(self, frame):
        frame.destroy()

# Executable section.
if __name__ == '__main__':

    root = Tk()
    root.title('U3T')

    client = Client(root)

    root.mainloop()

