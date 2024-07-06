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

win_count = 0 
game_count = 0
GAME_PLAYS = 1

for i in range(GAME_PLAYS):
    
    game_count += 1
    

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
                time.sleep(2.5)

    mullDecision(gameState,log)

    time.sleep(2)

    gameOver = False

    while not gameOver:
        while(gameState.phase != "Phase_Main1"):
            passPriority()
            time.sleep(.5)
            gameOver = checkMyTurn(gameState, log)
            if gameOver:
                print("Game Lost!")
                break
        
        if gameOver:
            break
        
        if(gameState.phase == "Phase_Main1"):
            print("--Playing Cards--")
            nextPlay = determineNextPlay(gameState)
            while(not nextPlay is None):
                playCardInHand(gameState, log, nextPlay)
                time.sleep(1.5)
                nextPlay = determineNextPlay(gameState)
            print("-----------------\n")
                
        time.sleep(1)
                
        passPriority()

        time.sleep(1)

        gameState.goTo("Phase_Combat")

        if(gameState.phase == "Phase_Combat"):
            attack()
            
        time.sleep(1)
        
        while(gameState.phase != "Opponent's Turn"):
            passPriority()
            time.sleep(.5)
            gameOver = checkMyTurn(gameState, log)
            if gameOver:
                win_count += 1
                print("Game Won!")
                break
    
    
    time.sleep(4)
    finishGame()
    time.sleep(4)
    
    print("Run Finished!")
    print("Total Games:", game_count)
    print("Total Wins:", win_count)
    print("Total Losses:", game_count - win_count)
    print("Win Rate:", (win_count + 0.0) / game_count)
    
# gameState.hand = []
# findHand(gameState, log)
# print(gameState.hand)

# \w+ AAAA \w+$     

# while True:
#     line = log.__next__()
#     if not line is None:
#         if "\"" in line:
#             print(line)
#             print("\n")


# play a turn: land, enchantment if available, creatures

