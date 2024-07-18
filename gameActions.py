import pyautogui as pag
import time
from GameState import *
import re

height = pag.size()[1]
width = pag.size()[0]

def moveTo(x, y, duration = 0.0):
    # print((x / 1920.0 * width, y / 1080.0 * height))
    pag.moveTo(x / 1920.0 * width, y / 1080.0 * height, duration)

def queue_recent():
    moveTo(1740, 1000, 1)
    time.sleep(0.1)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()
    
    time.sleep(0.5)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()

def mullDecision(gameState: GameState, log):
    landCount = 0
    for card in gameState.hand:
        if "Land" in card.data["type_line"]:
            landCount += 1
    if landCount > 1 and landCount < 5:
        moveTo(1140, 875) # change to keep 7 button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
    else:
        moveTo(800, 875) # change to mulligan button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
        gameState.hand = []
        findHand(gameState, log)
        moveTo(1140, 875) # change to keep 6 button
        time.sleep(2)
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
        moveTo(1250, 540)
        pag.mouseDown()
        moveTo(320, 540, 1)
        pag.mouseUp()
        moveTo(960, 875)
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()

def findCardInHand(log, target: Card):
    moveTo(100, 1070)
    searching = True
    while searching:
        
        pag.moveRel(100, 0, .1)
        # print("move Right")
        line = ""
        found = False
        while not found and not line is None:
            # print("finding hover message")
            line = log.__next__()
            # print(line)
            if not line is None:
                if "\"onHover\": {" in line and not r'"onHover": {}' in line:
                    # f = open("demofile2.txt", "a")
                    # f.write(str(line))
                    # f.close()
                    found = True
        if found:
            # print("found hover message")
            line = log.__next__()
            f = open("demofile2.txt", "a")
            f.write(str(line))
            f.close()
            search = re.search("objectId.: [0-9]+", line)
            id = int(search.group()[11:])
            # print(id)
            if target.instanceId == id:
                searching = False
        
        elif pag.position()[0] > 1660 / 1920.0 * width:
            # print("Not In Hand!\n")
            return False
    # print("Found Card!\n")
    return True

def determineNextPlay(gameState: GameState):
    print("--Hand--")
    for card in gameState.hand:
        print(card.data["name"])
    print("--------")
    card: Card
    permanent: Permanent
    untappedLands = 0
    for permanent in gameState.myBoard:
        if "Land" in permanent.data["type_line"] and permanent.untapped:
            untappedLands += 1
    print("Open mana:", untappedLands)
    print("Land drop available:", gameState.landDrop)
    for card in gameState.hand:
        if "Land" in card.data["type_line"] and gameState.landDrop:
            gameState.playedLand()
            print("Play land")
            return card
    for card in gameState.hand:
        if "Enchantment" in card.data["type_line"]:
            if card.data["name"] == "Cavalcade of Calamity" and untappedLands >= 2:
                print("Play cavalcade")
                return card
            elif card.data["name"] == "Raid Bombardment" and untappedLands >= 3:
                print("Play raid")
                return card
    for card in gameState.hand:
        if "Creature" in card.data["type_line"] and untappedLands >= 1:
            print("Play creature")
            return card
    print("No playable cards")
    return None

def playCardInHand(gameState: GameState, log, nextPlay: Card):
    inHand = findCardInHand(log, nextPlay)
    if inHand:
        gameState.playCard(nextPlay)
        time.sleep(.5)
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
    else:
        gameState.hand.remove(nextPlay)
    moveTo(100, 1070)
            
def passPriority():
    pag.keyDown("space")
    time.sleep(0.1)
    pag.keyUp("space")
    
def finishGame():
    moveTo(960, 540)
    pag.click()

def attack():
    time.sleep(1)
    moveTo(100, 1070)
    pag.keyDown("space")
    time.sleep(0.1)
    pag.keyUp("space")
    pag.keyDown("space")
    time.sleep(0.1)
    pag.keyUp("space")