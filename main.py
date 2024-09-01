import pyautogui as pag
import time
from GameState import *
from gameActions import * 
from logReading import *


# tracks the MTGA log file and returns a generator

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
#         if '{ "transactionId":' in line:
#         # if '[UnityCrossThreadLogger]' in line and 'GreToClientEvent' in line:
#             # print(line)
#             # line = log.__next__()
#             if 'turnInfo' in line:
#                 print("Recieved Priority")
#                 print(line)
#             else:
#                 print("SOMETHING HAPPENED AND I DIDNT GET PRIORITY")
#                 print(line)
        # gameObjects = re.search('"gameObjects": [ { .+? } ]', line)
        # if gameObjects is not None:
        #     gameObjects = gameObjects.group()
        #     print(gameObjects)
    # if line is not None:
    #     print(line)

gameState = GameState()
    
queue_recent()

findHand(gameState, log)
if gameState.turn == 'Self':
    wait = True
    while wait:
        line = log.__next__()
        if not line is None:
            check = re.search("Timer PregameSequence end", line)
            if not check is None:
                wait = False
                time.sleep(2.5)
else:
    wait = True
    while wait:
        line = log.__next__()
        if not line is None:
            check = re.search("GREMessageType_MulliganReq", line)
            if not check is None:
                wait = False
                time.sleep(2.5)
    



mullDecision(gameState,log)



time.sleep(2)







while True:
    line = log.__next__()
    
    analyzeLine(gameState, log, line)

