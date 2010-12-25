# main games
import thread
import serial
from game import *
import socket
import threading
import time
import wsserve

SERIALLOG = 'slog.log'
GAMELOG = 'glog.log'
PSCORES = 'pscores' # +num etc
TSCORES = 'tscores.json'

game = 0

def main():
    global game
    print "Starting up"
    print "Connecting to xbee... "
    xbee = xConnect()
    
    numPlayers = 16
    numTeams = 2
    xbee.flushInput()

    print "Creating a new game"
    game = Game(numPlayers,numTeams,15,15)
    
    print "Starting serial monitor"
    thread.start_new_thread(monitorSerial,(xbee,))
    print "Starting socket server"
    thread.start_new_thread(wsserve.start,(socketCommand,))

    server = startServer()
    writeSerial(xbee,'i44')
    time.sleep(1)
    writeSerial(xbee,'s')
        
    
    run = True
    while run:
        cin = raw_input(">>> ")
        if cin == 'stop':
            run = False
        print command(cin, game)
        time.sleep(.1)
    server.shutdown()

def socketCommand(commandstr = 'score'):
    global game
    return command(commandstr,game)

def command(command,game = game):
    command = command.split()
    if command[0] == "kill":
        return game.kill(int(command[1]),int(command[2]))
    
    elif command[0] == "endround":
        if not game.active:
            return "Game is not active"
        game.endRound()
        return "Game ended"

    elif command[0] == "score":
        return getScore(game)

    elif command[0] == "players":
        return str(game.players)
    
    elif command[0] == "time":
        return game.getTime()
    
    elif command[0] == "startgame":
        if game.active:
            return "Game already started"
        thread.start_new_thread(writeXml,(game,))
        game.startGame()
        return "Game Started"

    elif command[0] =="isGameActive":
        return game.active

    elif command[0] =="start":
        return ""
    
    elif command[0] == "stopserve":
        server.shutdown()
        return "server.shutdown sent"
    else:
        return "nothing"

def log(filename,string):
    print ">> " + string
    f = open(filename,'a')
    f.write(string + '\n')
    f.close()

def readPacket(ser):
    packet = ''
    started = False
    ended = False

    while ser.inWaiting() > 0:
        nextByte = ser.read()
        time.sleep(.001)
        if nextByte == '<':
            started = True
        elif nextByte == '>':
            ended = True
        else:
            packet += nextByte
        if started and ended:
            log(SERIALLOG,packet)
            return packet

    if started and ended:
        log(SERIALLOG,packet)
        return packet
    
    log(SERIALLOG,"error " + packet)
    return "error"
'''
def writeXml(game):
    initTeam()
    while(True):
        writePlayers(game)
        writeTeamScore(game)
        time.sleep(2)

def writeTeamScore(game):
    f = open(TSCORES,'r')
    totalString = f.read()
    f.close()
    f = open(TSCORES,'w')
    f.write(totalString[:-2]+ ',' + str(getScore(game)) +']}')
    f.close

def initTeam():
    f = open(TSCORES,'w')
    totalString = '{ "scores": [[0,[0,0],[0,1]]]}'
    f.write(totalString)
    f.close 

    
def writePlayers(game):
    for x in range(len(game.teams)):
        f = open(PSCORES+str(x)+'.json','w')
        totalString = '{ "aaData": ['
        for player in game.getPlayers():
            if player.getTeamNum() == x:
                string = '[' 
                string += str(player.pNum) + ','
                string += '"' + player.pName + '",'
                string += str(player.kills) + ','
                string += str(player.deaths) + '],'
                totalString += string

        totalString = totalString[:-1] + ']}'
        f.write(totalString)
        f.close()
     
'''


def findPlayers():
    # lol
    return input("placeholder.. enter num players.. ")

def xConnect():
    ser = serial.Serial('/dev/ttyUSB0',57600,timeout=1)
    time.sleep(1)
    ser.write("<a>")
    if ser.inWaiting()>0:
        ser.flushInput()
        print 'connected!'
        return ser
    else:
        print 'no connection'
        return xConnect()

def writeSerial(ser,string):
    ser.write("<")
    for char in string:
        ser.write(string)
    ser.write(">")

def monitorSerial(ser):
    while(True):
        time.sleep(5)
        while ser.inWaiting()>0:
            data = ser.readline()
            if not data=="\n":
                processSerial(data)
                print "\t\t\t >>" + data[:-1]

    return

def processSerial(data):
    data = data[1:-3]
    data = data.split()
    if len(data) > 0:
        if data[0] == 'k':
            print commandServe("kill " + data[1] + " " + data[2])
    return
'''
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "%s wrote:" % self.client_address[0]
        print self.data
        # just send back the same data, but upper-cased
        self.request.send(commandServe(self.data))


def startServer(host = "localhost",port=4242):
    server = SocketServer.TCPServer((host, port), MyTCPHandler)
    thread.start_new_thread(server.serve_forever,())
    return server
'''

if __name__== "__main__":
    main()


