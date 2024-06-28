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

def mullDecision(gameState, log):
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
        moveToBetter(1140, 875) # change to keep 7 button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()

def findCardInHand(gameState, log, target: Card):
    # print(target.instanceId)
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
            print(id)
            if target.instanceId == id:
                searching = False
        elif pag.position()[0] > 1660 / 1920.0 * width:
            return False
    return True