# main game setup
import math
from player import *
from team import *
import datetime

DEBUG=True

class Game:
    def __init__(this,numPlayers,numTeams,ammo,gameTime):
        ''' num players, ammo to give per reload, game time in minutes'''
        this.numPlayers = numPlayers
        this.numTeams = numTeams 
        this.teams = []
        this.players = []
        this.active = False
        this.ammo = ammo
        this.gameTime = gameTime
        this.startTime = 0
        this.mult = 10        
        # Create players
        for x in range(this.numPlayers):
            newPlayer = Player(42,x)
            this.players.append(newPlayer)

        # Create teams
        for x in range(this.numTeams):
            newTeam = Team(x)
            this.teams.append(newTeam)

        # Assign players to teams
        tempCount = 0
        for player in this.players:
            this.teams[tempCount].addPlayer(player)
            tempCount += 1
            if tempCount == this.numTeams:
                tempCount = 0

    def getPlayer(this,num):
        for player in this.players:
            if player.pNum == num:
                return player

        if DEBUG: print "Invalid Player: " + num
        return -1

    def isActive(this):
            return this.active

    def kill(this,shooterNum,targetNum):
        shooter = this.getPlayer(shooterNum)
        target = this.getPlayer(targetNum)
        shooter.gotKill()
        target.wasShot()
        return shooter.__repr__() + ' --shoots-> ' + target.__repr__()
    
    def startGame(this):
        this.active=True
        this.startTime = datetime.datetime.now()
        print 'blah blah blah'

    def getPlayers(this):
        return this.players

    def endRound(this):
        this.active=False
        for player in this.players:
            player.roundEnd()
    
    def getTime(this):
        dtime = datetime.datetime.now() - this.startTime
        return int(dtime.total_seconds())

    def getScore():
        teamscores = []
        for team in this.teams:
            teamscores.append([team,team.getScore()])

        return teamscores 

