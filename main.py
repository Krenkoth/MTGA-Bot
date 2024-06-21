import pyautogui as pag
import time

def queue_recent():
    pag.moveTo(1740, 1000)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()
    
    time.sleep(0.1)
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()


queue_recent()
