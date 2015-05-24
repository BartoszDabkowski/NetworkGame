__author__ = 'Xiaoyu'
from socket import *
import string

# initialize variables
game_list = []

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
        #current.creator = addr
        current.player = 'Waiting'
        game_list.append(current)
        newGameID += 1
        current.ID = newGameID
        current.name = 'Game ' + str(current.ID)

        port = str(int(port) + 1)

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

        # remove entry from game list
        for game in game_list:
            if game.ID == string.atoi(gameID):
                game_list.remove(game)
        print_game_list()

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



    print 'msg sent'

    connectionSocket.close()
    print('closed')


serverSocket.close()