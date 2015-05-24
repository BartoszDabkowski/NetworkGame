__author__ = 'Xiaoyu'
from socket import *
import string
import random

# initialize variables
game_list = []
score_board = []

# single entry on score board
class ScoreEntry:
    def __init__(self):
        self.player = ""
        self.score = 0

newGameID = 0

# game pairs
class GamePair:
    def __init__(self):
        self.ID = 0
        self.name = ''
        self.creator = ''
        self.player = ''

"""
current = GamePair()
current.creator = '12345'
current.player = 'Waiting'
game_list.append(current)
gameID += 1
current.ID = gameID
current.name = 'Game ' + str(current.ID)

current = GamePair()
current.creator = '6789'
current.player = 'Waiting'
game_list.append(current)
gameID += 1
current.ID = gameID
current.name = 'Game ' + str(current.ID)
"""

# print game list
def print_game_list():
    for game in game_list:
        print '{0:1d} {1:10s} {2:20s} {3:20s}'.format(game.ID, game.name, game.creator, game.player)

#print_game_list()

def print_score_board():
    for entry in score_board[:10]:
        print entry.player, entry.score

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print'The game server is ready to receive'
title = 0

# keep looping
while 1:
    if title == 0:
        print '{0:1s} {1:10s} {2:20s} {3:20s}'.format('ID', 'NAME', 'CREATOR', 'PLAYER')
        title += 1

    connectionSocket, addr = serverSocket.accept()

    address = str(addr)
    first = address.find('\'')
    address = address[first + 1:]
    ip = address[:address.find('\'')]
    port = address[address.find(' ') + 1: address.find(')')]
    print('ip and port: ', ip, port)

    print('accepted')

    request = connectionSocket.recv(1024)
    print (request)

    # parse if it is join request/end request
    if request.find('_') > 0:
        request, gameID = request.split('_')

    # create game entry into game list
    if request == 'create':

        current = GamePair()
        current.player = 'Waiting'
        game_list.append(current)
        newGameID += 1
        current.ID = newGameID
        current.name = 'Game ' + str(current.ID)

        #port = str(int(port) - 1)

        port = str(random.randint(10000, 99999))

        newAddr = '(' + '\'' + ip + '\', ' + port + ')'
        current.creator = newAddr

        respond = str(current.ID) + '_' + port

        connectionSocket.send(respond)
        print_game_list()

    elif request == 'join':

        for game in game_list:
            if game.ID == string.atoi(gameID):
                #if pair exists
                if game.player != 'Waiting':
                    connectionSocket.send('Game Not Available')
                    print'ERROR: Game Not Available'
                else:

                    # add player addr to the game list
                    game.player = addr

                    # send creator addr back to player
                    response = str(game.creator)
                    connectionSocket.send(response)
                    print_game_list()
                    break

    elif request == 'end':

        # update game result
        gameID, result = gameID.split(' ')

        # remove entry from game list
        for game in game_list:
            if game.ID == string.atoi(gameID):

                if len(score_board) == 0:
                    if result == '1':
                        # add creator
                        firstEntry = ScoreEntry()
                        firstEntry.player = game.creator
                        firstEntry.score += 1
                        score_board.append(firstEntry)

                        # add player
                        secondEntry = ScoreEntry()
                        secondEntry.player = game.player
                        score_board.append(secondEntry)

                    else:
                        # add player
                        firstEntry = ScoreEntry()
                        firstEntry.player = game.player
                        firstEntry.score += 1
                        score_board.append(firstEntry)

                        # add creator
                        secondEntry = ScoreEntry()
                        secondEntry.player = game.creator
                        score_board.append(secondEntry)
                else:

                    creatorExist = 0
                    playerExist = 0

                    for entry in score_board:
                        if entry.player == game.creator:
                            creatorExist = 1
                            if result == '1':
                                entry.score += 1
                        if entry.player == game.player:
                            playerExist = 1
                            if result == '0':
                                entry.score += 1

                    if creatorExist == 0:
                        if result == '1':
                            # add creator
                            firstEntry = ScoreEntry()
                            firstEntry.player = game.creator
                            firstEntry.score += 1
                            score_board.append(firstEntry)

                        else:
                            # add creator
                            secondEntry = ScoreEntry()
                            secondEntry.player = game.creator
                            score_board.append(secondEntry)

                    if playerExist == 0:
                        if result == '0':
                            # add player
                            firstEntry = ScoreEntry()
                            firstEntry.player = game.player
                            firstEntry.score += 1
                            score_board.append(firstEntry)

                        else:
                            # add player
                            secondEntry = ScoreEntry()
                            secondEntry.player = game.player
                            score_board.append(secondEntry)

                game_list.remove(game)
        print_game_list()

        # sort score_board on key score
        score_board.sort(key=lambda x : x.score, reverse = True)

        print_score_board()

        response = 'result updated'
        connectionSocket.send(response)

    elif request == 'list':

        list = ""
        for game in game_list[:-1]:
            if game.player == 'Waiting':
                list += str(game.ID) + ' '
        if game_list[len(game_list) - 1].player == 'Waiting':
            list += str(game_list[len(game_list) - 1].ID)

        connectionSocket.send(list)
        print_game_list()

    elif request == 'top':

        msg = ''
        for entry in score_board[:-1]:
            msg += str(entry.player) + ' ' + str(entry.score) + ' '

        msg += str(score_board[len(score_board) - 1].player) + ' ' + str(score_board[len(score_board) - 1].score)

        connectionSocket.send(msg)
        print msg

    print 'msg sent'

    connectionSocket.close()
    print('closed')


serverSocket.close()