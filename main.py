import pyautogui as pag
import time
from GameState import *
from gameActions import *
# from mtga.set_data import all_mtga_cards



def follow(file):
    # print(file.tell())
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            continue
        yield line


# print(all_mtga_cards.find_one(66819))
f = open(
    "C:/Users/johng/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log"
)
print(f.readline())
# line = f.readline()
log = follow(f)
print(type(log))

gameState = GameState()
running = True
while running:
    
    queue_recent()

    findHand(gameState, log)

    mullDecision(gameState,log)
    
    
# while True:
    # file_path = 'C:/Users/johng/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log'
    # with open(file_path, 'r') as file:
    #     lines = file.read().splitlines()
    #     print(len(lines))

