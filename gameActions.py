import pyautogui as pag
import time
from GameState import *
import re

height = pag.size()[1]
width = pag.size()[0]

def moveToBetter(x, y, duration = 0.0):
    # print((x / 1920.0 * width, y / 1080.0 * height))
    pag.moveTo(x / 1920.0 * width, y / 1080.0 * height, duration)

def queue_recent():
    moveToBetter(1740, 1000)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()
    
    time.sleep(0.1)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()

def mullDecision(gameState: GameState, log):
    landCount = 0
    for card in gameState.hand:
        if "Land" in card.data["type_line"]:
            landCount += 1
    if landCount > 1 and landCount < 5:
        moveToBetter(1140, 875) # change to keep 7 button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
    else:
        moveToBetter(800, 875) # change to mulligan button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
        gameState.hand = []
        findHand(gameState, log)
        moveToBetter(1140, 875) # change to keep 6 button
        time.sleep(1)
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()

def findCardInHand(log, target: Card):
    moveToBetter(260, 1060)
    searching = True
    while searching:
        pag.moveRel(100, 0, .1)
        line = ""
        found = False
        while not found and not line is None:
            line = log.__next__()
            if not line is None:
                if "\"onHover\": {" in line and not "\"onHover\": {}" in line:
                    found = True
        if found:
            line = log.__next__()
            search = re.search("objectId.: [0-9]+", line)
            id = int(search.group()[11:])
            # print(id)
            if target.instanceId == id:
                searching = False
        elif pag.position()[0] > 1660 / 1920.0 * width:
            return False
    return True

def determineNextPlay(gameState: GameState):
    card: Card
    permanent: Permanent
    untappedLands = 0
    for permanent in gameState.myBoard:
        if "Land" in permanent.data["type_line"] and permanent.untapped:
            untappedLands += 1
    print("open mana:", untappedLands)
    print(gameState.landDrop)
    for card in gameState.hand:
        if "Land" in card.data["type_line"] and gameState.landDrop:
            gameState.playedLand()
            print("play land")
            return card
    for card in gameState.hand:
        if "Enchantment" in card.data["type_line"]:
            if card.data["name"] == "Cavalcade of Calamity" and untappedLands >= 2:
                print("play cavalcade")
                return card
            elif card.data["name"] == "Raid Bombardment" and untappedLands >= 3:
                print("play raid")
                return card
    for card in gameState.hand:
        if "Creature" in card.data["type_line"] and untappedLands >= 1:
            print("play creature")
            return card
    print("no playable cards")
    return None

def playCardInHand(gameState: GameState, log, nextPlay: Card):
    findCardInHand(log, nextPlay)
    gameState.playCard(nextPlay)
    pag.mouseDown()
    time.sleep(0.05)
    pag.mouseUp()
    pag.mouseDown()
    time.sleep(0.05)
    pag.mouseUp()
    i = 0
    for permanent in gameState.myBoard:
        if "Land" in permanent.data["type_line"] and permanent.untapped and i < int(nextPlay.data["cmc"]):
            permanent.tap()
            i += 1
            
def passPriority():
    pag.keyDown("space")
    pag.keyUp("space")

def attack():
    pag.keyDown("space")
    pag.keyUp("space")
    pag.keyDown("space")
    pag.keyUp("space")