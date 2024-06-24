

# phases are: begin, main1, main2, combat, oppTurn
# boards and hand are lists of permanent objects

class GameState:
    def __init__(self):
        self.phase = "pregame"
        self.hand = []
        self.landDrop = True
        self.myBoard = []
        self.oppBoard = []

    def drawCard(self, id):
        self.hand.append(id)
    
    def goTo(self, phase):
        self.phase = phase
        if phase == "begin":
            self.landDrop = True
            for perm in self.myBoard:
                perm.untap()
        if phase == "oppTurn":
            for perm in self.oppBoard:   
                perm.untap()
                
    def playedLand(self):
        self.landDrop = False

class permanent:
    def __init__(self, id):
        self.id = id
        self.untapped = True
    
    def tap(self):
        self.untapped = False

    def untap(self):
        self.untapped = True
