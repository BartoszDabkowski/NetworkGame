# CSS432 - Client
# Bethel Heo, Bartosz Dabkowski, Xiiaoyu Liang
#
# Client.py
# Program for the game, connection to server, and P2P connection

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from socket import *
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

        # img = PhotoImage(master=self.canvas, file="imageXO.gif", width=60, height=60)

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

        window = Toplevel()
        game = U3T_Game(window)

        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('127.0.0.1', 1899))

        self.gameOn = True;

        while(self.gameOn):
            msg = str(s.recv(1024), 'utf-8')
            print(msg)
            s.send(bytes('Goodbye', 'utf-8'))

        s.close()

        '''
        window.title('Select a game to join')

        listbox = Listbox(window)
        listbox.pack()
        '''
        '''
        # request game list from primary server
        s = socket.socket()
        s.connect((self.primaryServerHost, self.primaryServerPort))
        s.send(b'list')
        list = []
        s.recv(list)
        s.close()
        '''

        '''
        for item in ['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5']:
            listbox.insert(END, item)

        joinButton = Button(window, text='Join', command=lambda: self.client(window))
        joinButton.pack()

        closeButton = Button(window, text='Close', command=lambda: self.close(window))
        closeButton.pack()
        '''

    # join a game. Become the client.
    def client(self, window):
        window.destroy()
        window = Toplevel()
        window.title('U3T: Ultimate Tic-Tac-Toe game')

        '''
        # request from primary server the hostname and port number
        s = socket.socket()
        s.connect((self.primaryServerHost, self.primaryServerPort))
        s.send(b'gameinfo')
        gameinfo = s.recv(1024)
        s.close()
        '''

        # connect to server
        host = socket.gethostname() # replace with info from server
        port = 1899
        s = socket.socket()
        s.connect((host, port))

        self.gameOn = True

        gameLabel = Label(window, text='Game is going on')
        closeButton = Button(window, text='Close', command=lambda: self.closeAndQuit(window, s))
        gameLabel.pack()
        closeButton.pack()

        # game instance
        while(self.gameOn):
            s.send(bytes('test2', 'utf-8'))
            data = str(s.recv(1024), 'utf-8')
            print(data)

            s.send(bytes('test3', 'utf-8'))
            s.send(bytes('test4', 'utf-8'))
            s.send(bytes('quit', 'utf-8'))
            gameOn = False

        s.close()
        window.destroy()

    # start a new game
    def create(self):
        # new window for game. First will wait for a connection from new player

        window = Toplevel()

        '''
        waitingLabel = Label(window, text='Waiting for player')
        waitingLabel.pack()

        closeButton = Button(window, text='Close', command=lambda: self.close(window))
        closeButton.pack()
        '''
        '''
        # send information to primary server the local host and port number
        s = socket.socket()
        s.connect((self.primaryServerHost, self.primaryServerPort))

        host = socket.gethostname()
        port = 1899

        s.send(host, " ", port)
        s.close()
        '''

        game = U3T_Game(window)

        # become the server/host for a new game
        #messagebox.showinfo(title='Waiting', message='Waiting for player')
        port = 1899
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', port))
        s.listen(5)

        self.gameOn = True

        while(self.gameOn):
            c, addr = s.accept()

            coord = game.move()

            print(coord[0], coord[1])

            '''
            c.send(bytes('Hello', 'utf-8'))
            msg = str(c.recv(1024), 'utf-8')
            print(msg)
            '''

        c.close()


        '''
        self.gameOn = True;

        waitingLabel.config(text='Game is going on')
        closeButton.config(command=lambda: self.closeAndQuit(window, c))

        # game instance
        while(self.gameOn):
            c.send(bytes('test1', 'utf-8'))
            data = str(c.recv(1024), 'utf-8')
            waitingLabel.config(text=(data, " received"))

            # if the other player quits we win
            if data == 'quit':
                messagebox.showinfo(title='Winner', message='You won!')
                self.gameOn = False

        # game is over
        c.close()
        window.destroy()
        '''

    # exit/close window
    def close(self, frame):
        frame.destroy()

    # exit/close window and quit the game
    def closeAndQuit(self, frame, socket):
        quit = messagebox.askokcancel(title='Quit?', message='Are you sure you want to quit?')

        if quit == True:
            self.gameOn = False
            socket.send(bytes('quit', 'utf-8'))
            frame.destroy()
        else:
            return


# Executable section.
if __name__ == '__main__':

    root = Tk()
    root.title('U3T')

    client = Client(root)

    root.mainloop()

