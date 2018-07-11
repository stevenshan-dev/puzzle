from pynput.mouse import Button, Controller
from pynput import keyboard

import random
import time
import math
import os
import signal

# for arrows
CENTER = (640, 1530)
OFFSET = 100
ALERT = (1400, 410)

mouse = Controller()

def click(func = None):
    def _click():
        mouse.press(Button.left)
        mouse.release(Button.left)

    if func == None:
        _click() 
    else:
        def _func(*argv, **kwargs):
            temp = func(*argv, **kwargs)
            _click()
            return temp
        return _func
        

@click
def top():
    mouse.position =(CENTER[0], CENTER[1] - OFFSET)
@click
def bottom():
    mouse.position = (CENTER[0], CENTER[1] + OFFSET)
@click
def left():
    mouse.position = (CENTER[0] - OFFSET, CENTER[1])
@click
def right():
    mouse.position = (CENTER[0] + OFFSET, CENTER[1])
@click
def alert():
    mouse.position = ALERT

def on_press(key):
    char = "{0}".format(key.char)

moves = [top, bottom, left, right]


for i in range(100):
    move = random.randint(0, 3)
    moves[move]()    
    time.sleep(0.2)
    alert()
