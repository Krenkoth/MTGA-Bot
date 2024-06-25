import pyautogui as pag
import time
from GameState import *

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
        if "Land" in card["type_line"]:
            landCount += 1
    if landCount > 1 and landCount < 5:
        pag.moveTo(1740, 1000) # change to keep 7 button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
    else:
        pag.moveTo(1740, 1000) # change to mulligan button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()
        gameState.hand = []
        findHand(gameState, log)
        pag.moveTo(1740, 1000) # change to keep 7 button
        pag.mouseDown()
        time.sleep(0.1)
        pag.mouseUp()