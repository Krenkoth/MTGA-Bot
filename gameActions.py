import pyautogui as pag
import time
from GameState import *
import re

def queue_recent():
    pag.moveTo(1740, 1000)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()
    
    time.sleep(0.1)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()

def mullDecision(gameState, log):
    landCount = 0
    for card in gameState.hand:
        if "Land" in card.data["type_line"]:
            landCount += 1
    if landCount > 1 and landCount < 5:
        pag.moveTo(1140, 875) # change to keep 7 button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
    else:
        pag.moveTo(800, 875) # change to mulligan button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
        gameState.hand = []
        findHand(gameState, log)
        pag.moveTo(1140, 875) # change to keep 7 button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
    pag.moveTo(0, 0)

def findCardInHand(gameState, log, target):
    pag.moveTo(260, 1079)
    searching = True
    while searching:
        pag.moveRel(100, 0)
        line = ""
        found = False
        while not found and not line is None:
            line = log.__next__()
            if "\"onHover\": {" in line:
                found = True
        if found:
            line = log.__next__()
            search = re.search("objectId.: [0-9]+", line)
            id = int(search.group()[11:])
            for card in gameState.hand():
                if id == id:
                    searching = False
        elif pag.position[0] > 1660:
            return False
    return True
            
# def determineNextPlay(gameState):

