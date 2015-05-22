__author__ = 'Xiaoyu'

from socket import *


option = raw_input('Do you want to create or join or end? ')

# send its port number and keeps connection with server
# disconnect with server when pair matched
if option == 'create':

    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send('create')
    response = clientSocket.recv(1024)

    print('From Server:', response)

    while 1:
        response = clientSocket.recv(1024)
        if response == 'terminate': break
    clientSocket.close()

# send its port number and game id to server
# receive the creator id from server and disconnect
elif option == 'join':

    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    gameID = 1
    request = 'join_' + str(gameID)
    clientSocket.send(request)
    creatorID = clientSocket.recv(1024)

    print('From Server:', creatorID)
    clientSocket.close()

# creator contacts server to send game result
# send its addr to server and disconnect
elif option == 'end':

    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    gameID = 1
    request = 'end_' + str(gameID)
    clientSocket.send(request)
    response = clientSocket.recv(1024)
    print('From Server:', response)
    clientSocket.close()

else:
    print('invalid input')
