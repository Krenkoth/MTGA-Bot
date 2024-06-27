
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


class Permanent:
    def __init__(self, data, instanceId):
        self.data = data
        self.untapped = True
        self.instanceId = instanceId
    
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
        check = re.search("{ \"transactionId\":.+\"gameObjects\"", line)
        if not (check is None):
            found = True
    turn = re.search("turnInfo.: { .activePlayer.: [0-9]", line)
    turn = int(turn.group()[29])
    if turn == 1:
        gameState.moveTo("main1")
    else:
        gameState.moveTo("oppTurn")
    results = re.findall(r"\{ \"instanceId\": \d+, \"grpId\": \d+, .+?, \"zoneId\": 31", line)
    print(results)
    for card in results:
        search = re.search("grpId.: [0-9]+", card)
        link = "https://api.scryfall.com/cards/arena/" + search.group()[8:]
        instance = re.search("instanceId.: [0-9]+", card)
        response = requests.get(link)
        gameState.drawCard(Card(response.json(), int(instance.group()[13:])))
    for card in gameState.hand:
        print(card.data["name"])

# { "instanceId": 159, "grpId": 66819, "type": "GameObjectType_Card", "zoneId": 31, 
# "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, 
# "cardTypes": [ "CardType_Creature" ], "subtypes": [ "SubType_Goblin", 
# "SubType_Pirate" ], "color": [ "CardColor_Red" ], "power": { "value": 1 }, 
# "toughness": { "value": 1 }, "viewers": [ 1 ], "name": 181801, 
# "abilities": [ 9, 117109 ], "overlayGrpId": 66819, "skinCode": "DA", 
# "baseSkinCode": "DA" }