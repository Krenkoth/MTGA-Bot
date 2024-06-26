import pyautogui as pag
import time
from GameState import *
from gameActions import *



def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            continue
        yield line


f = open(
    "C:/Users/johng/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log"
)
log = follow(f)

gameState = GameState()
    
queue_recent()

findHand(gameState, log)

wait = True
while wait:
    line = log.__next__()
    check = re.search("Timer PregameSequence end", line)
    if not line is None:
        wait = False
        time.sleep(2)

mullDecision(gameState,log)

# play a turn: land, enchantment if available, creatures

