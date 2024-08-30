
import requests
import json
import time
import re


def getCard(id):
    link = "https://api.scryfall.com/cards/arena/" + id
    response = requests.get(link).json()
    if response["object"] == "card":
        return response
    else:
        link = "https://api.scryfall.com/cards/3186f5e2-8078-4fa3-b61e-866c2d4c495d?format=json"
        print("ERROR, assume Goblin Token")
        return requests.get(link).json()

class GameState:
    def __init__(self):
        self.goTo('Pregame', 'pregame', 'None')
        self.hand = []
        self.landDrop = True
        self.myBoard = []
        self.oppBoard = []

    def drawCard(self, card):
        self.hand.append(card)
        
    def playCard(self, card):
        self.hand.remove(card)
        self.myBoard.append(Permanent(card))
    
    def goTo(self, phase, step, turn):
        self.phase = phase
        self.turn = turn
        if turn == 1:
            self.turn = 'Self'
        elif turn == 2:
            self.turn = 'Opp'
        if step is None:
            self.step = "Main"
        else:
            self.step = step
        print("--Phase--")
        print(self.turn + " " + self.phase + " " + self.step)
        print("---------")
        if phase == "Phase_Beginning":
            self.landDrop = True
            for perm in self.myBoard:
                perm.untap()
            time.sleep(4)
        if phase == 'Phase_Beginning' and self.turn == "Opp":
            for perm in self.oppBoard:   
                perm.untap()
                
    def playedLand(self):
        self.landDrop = False


class Permanent:
    def __init__(self, card):
        self.data = card.data
        self.untapped = True
        self.instanceId = card.instanceId
    
    def tap(self):
        self.untapped = False

    def untap(self):
        self.untapped = True



class Card:
    def __init__(self, data, instanceId):
        self.data = data
        self.instanceId = instanceId


def findHand(gameState, log):
    found = False
    line = ""
    while not found:
        line = log.__next__()
        if not line is None:
            check = re.search("{ \"transactionId\":.+\"gameObjects\"", line)
            if not (check is None):
                found = True
    if gameState.phase == "Pregame":
        turn = re.search("turnInfo.: { .activePlayer.: [0-9]", line)
        turn = int(turn.group()[29])
        if turn == 1:
            gameState.goTo("Phase_Beginning", None, 'Self')
        else:
            gameState.goTo("Phase_Beginning", None, 'Opp')
    results = re.findall('{ "instanceId": [0-9]+, "grpId": [0-9]+, .+?, "zoneId": 31', line)
    for card in results:
        id = re.search("grpId.: [0-9]+", card).group()[8:]
        instance = re.search("instanceId.: [0-9]+", card)
        response = getCard(id)
        gameState.drawCard(Card(response, int(instance.group()[13:])))
    print("--Hand--")
    card: Card
    for card in gameState.hand:
        print(card.data["name"], card.instanceId)
    print("--------\n")
        
def getCardDraw(gameState, line):
    if not line is None:
        results = re.findall(r".type.: .ZoneType_Library.+?, \"zoneId\": 31.", line)
        for cardInfo in results:
            search = re.search("grpId.: [0-9]+", cardInfo)
            link = "https://api.scryfall.com/cards/arena/" + search.group()[8:]
            instance = re.search("instanceId.: [0-9]+", cardInfo)
            instanceId = int(instance.group()[13:])
            response = requests.get(link)
            inHand = False
            card: Card
            for card in gameState.hand:
                if instanceId == card.instanceId:
                    inHand = True
            if not inHand:
                gameState.drawCard(Card(response.json(), instanceId))
        print("--Hand--")
        card: Card
        print(gameState.hand)
        for card in gameState.hand:
            print(card.data)
            print(card.data["name"], card.instanceId)
        print("--------\n")
        
def checkMyTurn(gameState, log):
    found = False
    line = ""
    while not found and not line is None:
        line = log.__next__()
        if not line is None:
            check = re.search("{ \"transactionId\":.+.phase.: .Phase_Beginning.", line)
            # f = open("demofile2.txt", "a")
            # f.write(str(line))
            # f.close()
            if not (check is None):
                found = True
            check = re.search("MatchEndScene", line)
            if not (check is None):
                return True
    if not line is None:
        turn = re.search(".phase.: .Phase_Beginning., .+?.activePlayer.: [0-9]", line)
        print(turn.group())
        turn = int(turn.group()[len(turn.group()) - 1])
        print(turn)
        if turn == 2:
            gameState.goTo("Opponent's Turn")
        else:
            gameState.goTo("Phase_Beginning")
            getCardDraw(gameState, line)
    return False

# { "instanceId": 159, "grpId": 66819, "type": "GameObjectType_Card", "zoneId": 31, 
# "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, 
# "cardTypes": [ "CardType_Creature" ], "subtypes": [ "SubType_Goblin", 
# "SubType_Pirate" ], "color": [ "CardColor_Red" ], "power": { "value": 1 }, 
# "toughness": { "value": 1 }, "viewers": [ 1 ], "name": 181801, 
# "abilities": [ 9, 117109 ], "overlayGrpId": 66819, "skinCode": "DA", 
# "baseSkinCode": "DA" }