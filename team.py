# Teams

class Team:
    def __init__(this,teamNum):
        this.teamNum = teamNum
        this.players = []
        this.score = 0

    def addPlayer(this,player):
        player.setTeam(this.teamNum)
        this.players.append(player)

    def __repr__(this):
        return "Team: " + str(this.teamNum) + " Players: " \
        + str(len(this.players)) 

    def getScore(this):
        totscore = 0
        for player in this.players:
            totscore += player.getScore()

        totscore += this.score
        return totscore
