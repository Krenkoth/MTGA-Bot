import pyautogui as pag
import time
# from mtga.set_data import all_mtga_cards

def queue_recent():
    pag.moveTo(1740, 1000)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()
    
    time.sleep(0.1)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()

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
print(log.__next__())
while True:
    # try:
    line = log.__next__()
    print(line)
    # except S
# while True:
    # file_path = 'C:/Users/johng/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log'
    # with open(file_path, 'r') as file:
    #     lines = file.read().splitlines()
    #     print(len(lines))

