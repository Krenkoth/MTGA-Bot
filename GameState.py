
import requests
import json
import time
import re
# phases are: begin, main1, main2, combat, oppTurn
# boards and hand are lists of permanent objects

class GameState:
    def __init__(self):
        self.phase = "pregame"
        self.hand = []
        self.landDrop = True
        self.myBoard = []
        self.oppBoard = []

    def drawCard(self, card):
        self.hand.append(card)
        
    def playCard(self, card):
        self.hand.remove(card)
        self.myBoard.append(Permanent(card))
    
    def goTo(self, phase):
        self.phase = phase
        print(phase)
        if phase == "Phase_Begin":
            self.landDrop = True
            for perm in self.myBoard:
                perm.untap()
            time.sleep(2)
            self.goTo("Phase_Main1")
        if phase == "oppTurn":
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
    turn = re.search("turnInfo.: { .activePlayer.: [0-9]", line)
    turn = int(turn.group()[29])
    if turn == 1:
        gameState.goTo("Phase_Main1")
    else:
        gameState.goTo("oppTurn")
    results = re.findall(r"\{ \"instanceId\": \d+, \"grpId\": \d+, .+?, \"zoneId\": 31", line)
    print(results)
    card: Card
    for card in results:
        search = re.search("grpId.: [0-9]+", card)
        link = "https://api.scryfall.com/cards/arena/" + search.group()[8:]
        instance = re.search("instanceId.: [0-9]+", card)
        response = requests.get(link)
        gameState.drawCard(Card(response.json(), int(instance.group()[13:])))
    for card in gameState.hand:
        print(card.data["name"], card.instanceId)
        
def checkMyTurn(gameState, log):
    found = False
    line = ""
    while not found and not line is None:
        line = log.__next__()
        if not line is None:
            check = re.search("\"phase\": \"Phase_Ending\"", line)
            if not (check is None):
                found = True
    if not line is None:
        turn = re.search(".activePlayer.: [0-9]", line)
        turn = int(turn.group()[16])
        if turn == 1:
            gameState.goTo("oppTurn")
        else:
            
            gameState.goTo("Phase_Begin")

# { "instanceId": 159, "grpId": 66819, "type": "GameObjectType_Card", "zoneId": 31, 
# "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, 
# "cardTypes": [ "CardType_Creature" ], "subtypes": [ "SubType_Goblin", 
# "SubType_Pirate" ], "color": [ "CardColor_Red" ], "power": { "value": 1 }, 
# "toughness": { "value": 1 }, "viewers": [ 1 ], "name": 181801, 
# "abilities": [ 9, 117109 ], "overlayGrpId": 66819, "skinCode": "DA", 
# "baseSkinCode": "DA" }