# CSS432 - Client
# Bethel Heo, Bartosz Dabkowski, Xiiaoyu Liang
#
# Client.py
# Program for the game, connection to server, and P2P connection

from tkinter import *
from PIL import Image, ImageTk

class Client(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master    = master

        # create main frame
        mainFrame = Frame(master, width=700, height=700)
        mainFrame.pack()

        # create title label from image
        titleImage = Image.open('title.jpg')
        titlePhoto = ImageTk.PhotoImage(titleImage)
        titleLabel = Label(mainFrame, image=titlePhoto)
        titleLabel.image = titlePhoto
        titleLabel.pack()

        # create join button
        joinImage = Image.open('join.jpg')
        joinPhoto = ImageTk.PhotoImage(joinImage)
        joinButton = Button(mainFrame, image=joinPhoto, command=lambda: self.join())
        joinButton.image = joinPhoto
        joinButton.pack()

        # create create button
        createImage = Image.open('create.jpg')
        createPhoto = ImageTk.PhotoImage(createImage)
        createButton = Button(mainFrame, image=createPhoto, command=lambda: self.create())
        createButton.image = createPhoto
        createButton.pack()

        # create exit button
        exitImage = Image.open('exit.jpg')
        exitPhoto = ImageTk.PhotoImage(exitImage)
        exitButton = Button(mainFrame, image=exitPhoto, command=lambda: self.close(self.master))
        exitButton.image = exitPhoto
        exitButton.pack()

    # join game
    def join(self):
        window = Toplevel()
        window.title('Select a game to join')

        listbox = Listbox(window)
        listbox.pack()

        for item in ['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5']:
            listbox.insert(END, item)

        joinButton = Button(window, text='Join')
        joinButton.pack()

        closeButton = Button(window, text='Close', command=lambda: self.close(window))
        closeButton.pack()

    # start a new game
    def create(self):
        window = Toplevel()
        window.title('Lets Goooooo')
        gameLabel = Label(window, text='Game goes here')
        gameLabel.pack()

        closeButton = Button(window, text='Close', command=lambda: self.close(window))
        closeButton.pack()

    # exit/close window
    def close(self, frame):
        frame.destroy()

# Executable section.
if __name__ == '__main__':

    root = Tk()
    root.title('U3T')

    client = Client(root)

    root.mainloop()
