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
        game = U3T_Game(window, 'join')


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

    # start a new game
    def create(self):
        # new window for game
        window = Toplevel()
        game = U3T_Game(window, 'create')


        '''
        c, addr = s.accept()

        c.send(bytes('Hello', 'utf-8'))
        msg = str(c.recv(1024), 'utf-8')
        print(msg)

        c.close()

        # send information to primary server the local host and port number
        s = socket.socket()
        s.connect((self.primaryServerHost, self.primaryServerPort))

        host = socket.gethostname()
        port = 1899

        s.send(host, " ", port)
        s.close()

        c.send(bytes('test1', 'utf-8'))
        data = str(c.recv(1024), 'utf-8')
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

