import pyautogui as pag
from main import follow


f = open(
    "C:/Users/johng/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log"
)
log = follow(f)
    
while True:
    print(log.__next__())

    # 260, 1070
    # 1660, 1070