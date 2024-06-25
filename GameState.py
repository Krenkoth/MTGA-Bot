
import requests
import json
import time
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


class permanent:
    def __init__(self, id):
        self.id = id
        self.untapped = True
    
    def tap(self):
        self.untapped = False

    def untap(self):
        self.untapped = True

import re

def findHand(gameState, log):
    found = False
    line = ""
    while not found:
        line = log.__next__()
        check = re.search("{ \"transactionId\":.+\"gameObjects\"", line)
        if not (check is None):
            found = True
            print(line)
    results = re.findall(r"\{ \"instanceId\": \d+, \"grpId\": \d+, .+?, \"zoneId\": 31", line)
    for card in results:
        search = re.search("grpId\": [:digit:]+")
        link = "https://api.scryfall.com/cards/arena/" + search.group()
        response = requests.get(link)
        gameState.drawCard(response.json())
    for card in gameState.hand:
        print(card["name"])

# { "instanceId": 159, "grpId": 66819, "type": "GameObjectType_Card", "zoneId": 31, 
# "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, 
# "cardTypes": [ "CardType_Creature" ], "subtypes": [ "SubType_Goblin", 
# "SubType_Pirate" ], "color": [ "CardColor_Red" ], "power": { "value": 1 }, 
# "toughness": { "value": 1 }, "viewers": [ 1 ], "name": 181801, 
# "abilities": [ 9, 117109 ], "overlayGrpId": 66819, "skinCode": "DA", 
# "baseSkinCode": "DA" }