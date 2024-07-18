import pyautogui as pag
import time
from GameState import *
from gameActions import *


# tracks the MTGA log file and returns a generator
def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if line is None or not line:
            yield None
            continue
        yield line
name = "johng"
link = "C:/Users/" + name + "/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log"
f = open(link)
log = follow(f)
line = ""

# while True:
#     print(pag.position())

# while True:
#     line = log.__next__()
#     if not line is None:
#         print(line)

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
            time.sleep(2.5)

mullDecision(gameState,log)

time.sleep(2)







while True:
    line = log.__next__()
    

    # If there is a new line in the log file
    

        # else:
            # print(line)
                
                    
                        




    # while(gameState.phase != "Phase_Main1"):
    #     checkMyTurn(gameState, log)
    # if(gameState.phase == "Phase_Main1"):
    #     nextPlay = determineNextPlay(gameState)
    #     while(not nextPlay is None):
    #         playCardInHand(gameState, log, nextPlay)
    #         time.sleep(1)
    #         nextPlay = determineNextPlay(gameState)
            
    # time.sleep(1)
            
    # passPriority()

    # time.sleep(1)

    # gameState.goTo("Phase_Combat")

    # if(gameState.phase == "Phase_Combat"):
    #     attack()
        
    # time.sleep(1)
    
    # while(gameState.phase != "oppTurn"):
    #     passPriority()
    #     time.sleep(.5)
    #     checkMyTurn(gameState, log)
    # print("endTurn")




# play a turn: land, enchantment if available, creatures

