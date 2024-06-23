import pyautogui as pag
import time
from mtga.set_data import all_mtga_cards

def queue_recent():
    pag.moveTo(1740, 1000)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()
    
    time.sleep(0.1)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()

# print(all_mtga_cards.find_one(66819))

while True:
    file_path = 'C:/Users/johng/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log'
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
        print(len(lines))

