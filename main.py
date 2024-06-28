import pyautogui as pag
import time
from GameState import *
from gameActions import *



def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            yield None
        yield line


f = open(
    "C:/Users/willi/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log"
)
log = follow(f)

gameState = GameState()
    
queue_recent()

findHand(gameState, log)

wait = True
while wait:
    line = log.__next__()
    if not line is None:
        check = re.search("Timer PregameSequence end", line)
        if not check is None:
            wait = False
            time.sleep(2)

mullDecision(gameState,log)

time.sleep(2)

findCardInHand(gameState, log, gameState.hand[5])

# determineNextPlay(gameState)


# play a turn: land, enchantment if available, creatures

