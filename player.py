# Player class for laser tag

class Player:
    def __init__(this,teamNum,playerNum):
        this.teamNum = teamNum
        this.pNum = playerNum
        this.pName = 'Beast'
        this.hp = 100
        this.kills = 0
        this.shots = 0
        this.deaths = 0
        this.hits = 0
        this.active = False
        this.score = 0

    def __repr__(this):
        string = ''
        string += "Team: " + str(this.teamNum)
        string += " Player: " + str(this.pNum)
        string += " Kills: " + str(this.kills)
        string += " Deaths: " + str(this.deaths)

        return string

    def getTeamNum(this):
        return this.teamNum

    def wasShot(this):
        this.deaths += 1

    def gotKill(this):
        this.kills += 1

    def setTeam(this,x):
        this.teamNum = x

    def getScore(this):
        return this.score + this.kills

    def roundStart(this):
        this.active = True

    def roundEnd(this):
        this.active = False
